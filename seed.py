"""Create leads.db and fill it with sample data. Safe to re-run."""
import hashlib
import os
import sqlite3

from config import Config


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


USERS = [
    # id, username, password, full_name, role
    (1, "admin", "admin123", "Priya Admin", "admin"),
    (2, "alice", "password1", "Alice Rep", "sales"),
    (3, "bob", "letmein", "Bob Rep", "sales"),
]

LEADS = [
    # owner_id, name, company, email, phone, status, value, notes
    (2, "Maya Chen", "Northwind Fabrics", "maya.chen@example.com", "555-0101", "New", 12000,
     "Met at the trade show. Interested in the <b>annual</b> plan."),
    (2, "Jordan Ellis", "Bluepeak Logistics", "jordan@example.org", "555-0102", "Contacted", 8500,
     "Wants a demo next Tuesday."),
    (2, "Sam Okafor", "Quill & Ink Co.", "sam.okafor@example.net", "555-0103", "Qualified", 23000,
     "Budget approved, waiting on legal."),
    (3, "Lena Varga", "Harbor Health", "lena.varga@example.com", "555-0201", "New", 41000,
     "Referred by Dr. Patel. Very price sensitive."),
    (3, "Theo Brandt", "Brandt Motors", "theo@example.org", "555-0202", "Negotiation", 67000,
     "Asked for 20% discount. CONFIDENTIAL: competitor quoted $52k."),
    (3, "Ana Ruiz", "Sunfield Farms", "ana.ruiz@example.net", "555-0203", "Lost", 5000,
     "Went with another vendor."),
    (1, "Kofi Mensah", "Mensah Capital", "kofi@example.com", "555-0301", "Qualified", 120000,
     "Strategic account - exec sponsor is the CEO."),
]


def init_db(path=Config.SQLITE_PATH):
    if os.path.exists(path):
        os.remove(path)
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT,
            role TEXT
        );
        CREATE TABLE leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER REFERENCES users(id),
            name TEXT,
            company TEXT,
            email TEXT,
            phone TEXT,
            status TEXT,
            value INTEGER,
            notes TEXT
        );
        """
    )
    conn.executemany(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
        [(i, u, md5(p), n, r) for i, u, p, n, r in USERS],
    )
    conn.executemany(
        "INSERT INTO leads (owner_id, name, company, email, phone, status, value, notes) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        LEADS,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Seeded {Config.SQLITE_PATH}")
