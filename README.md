> **⚠️ WARNING: THIS APPLICATION IS DELIBERATELY INSECURE.**
> **It was built only as a target for a classroom security demo (in the spirit of OWASP DVWA / Juice Shop).**
> **NEVER deploy it to the public internet or any shared network. Run it on localhost only.**
> **It contains NO real secrets — every key, token, and password in this repo is a fake placeholder.**

# LeadLoop

A tiny lead-tracking app: sign in, see your leads, search them, open a lead and keep notes on it.

Built with Python, Flask, and a local SQLite file. No external services are used.

## Run it locally

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed.py        # creates leads.db with sample data (also auto-created on first run)
flask run             # http://127.0.0.1:5000
```

`flask run` binds to `127.0.0.1` by default. Do not pass `--host 0.0.0.0`.

## Sample accounts

| Username | Password  | Role  |
|----------|-----------|-------|
| admin    | admin123  | admin |
| alice    | password1 | sales |
| bob      | letmein   | sales |

## Resetting

Delete `leads.db` (or run `python seed.py` again) to restore the sample data.
