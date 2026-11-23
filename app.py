import hashlib
import os
import traceback

from flask import Flask, redirect, render_template, request, session, url_for, jsonify

from config import Config
from datastore import get_client
from seed import init_db

app = Flask(__name__)
app.config.from_object(Config)

if not os.path.exists(Config.SQLITE_PATH):
    init_db()


def current_user():
    return session.get("user")


@app.before_request
def require_login():
    open_endpoints = {"login", "static", "internal_export", "health"}
    if request.endpoint not in open_endpoints and not current_user():
        return redirect(url_for("login", next=request.path))


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        pw_hash = hashlib.md5(password.encode()).hexdigest()

        db = get_client()
        sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{pw_hash}'"
        user = db.query_one(sql)
        db.close()

        if user:
            session["user"] = {
                "id": user["id"],
                "username": user["username"],
                "full_name": user["full_name"],
                "role": user["role"],
            }
            return redirect(request.args.get("next") or url_for("leads"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    return redirect(url_for("leads"))


@app.route("/leads")
def leads():
    user = current_user()
    db = get_client()
    rows = db.query(f"SELECT * FROM leads WHERE owner_id = {user['id']} ORDER BY id")
    db.close()
    return render_template("leads.html", leads=rows, user=user)


@app.route("/search")
def search():
    user = current_user()
    q = request.args.get("q", "")
    db = get_client()
    sql = (
        "SELECT * FROM leads WHERE owner_id = " + str(user["id"]) +
        " AND (name LIKE '%" + q + "%' OR company LIKE '%" + q + "%') ORDER BY id"
    )
    try:
        rows = db.query(sql)
    except Exception as e:
        return render_template(
            "error.html",
            message=str(e),
            query=sql,
            trace=traceback.format_exc(),
        ), 500
    finally:
        db.close()
    return render_template("search.html", leads=rows, q=q, user=user)


@app.route("/lead/<int:lead_id>", methods=["GET", "POST"])
def lead_detail(lead_id):
    user = current_user()
    db = get_client()
    if request.method == "POST":
        db.execute("UPDATE leads SET notes = ? WHERE id = ?", (request.form.get("notes", ""), lead_id))
    lead = db.query_one(f"SELECT * FROM leads WHERE id = {lead_id}")
    db.close()
    if lead is None:
        return render_template("error.html", message="Lead not found"), 404
    return render_template("lead.html", lead=lead, user=user)


@app.route("/internal/export")
def internal_export():
    db = get_client()
    data = {
        "users": db.query("SELECT * FROM users"),
        "leads": db.query("SELECT * FROM leads"),
    }
    db.close()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
