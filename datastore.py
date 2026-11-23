"""Thin data-access client.

Mirrors the interface of the hosted client we plan to move to, so swapping
SQLite for the real backend later is a one-file change.
"""
import sqlite3

from config import Config

ROLES = {
    Config.SUPABASE_ANON_KEY: "anon",
    Config.SUPABASE_SERVICE_KEY: "service_role",
}


class DataClient:
    def __init__(self, api_key):
        self.role = ROLES.get(api_key)
        if self.role is None:
            raise PermissionError("invalid API key")
        self.conn = sqlite3.connect(Config.SQLITE_PATH)
        self.conn.row_factory = sqlite3.Row

    def query(self, sql):
        cur = self.conn.execute(sql)
        return [dict(r) for r in cur.fetchall()]

    def query_one(self, sql):
        rows = self.query(sql)
        return rows[0] if rows else None

    def execute(self, sql, params=()):
        if self.role != "service_role":
            raise PermissionError("write requires service_role")
        self.conn.execute(sql, params)
        self.conn.commit()

    def close(self):
        self.conn.close()


def get_client():
    return DataClient(Config.SUPABASE_SERVICE_KEY)
