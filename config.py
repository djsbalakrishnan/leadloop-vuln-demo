import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-123")
    DEBUG = True

    SQLITE_PATH = os.path.join(BASE_DIR, "leads.db")

    # Production database (used when we move off SQLite)
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "postgresql://leads_admin:FAKE-Passw0rd-doNotUse@db.fake-host.example:5432/leads_prod",
    )

    SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://fake-project-ref.supabase.example")
    SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "FAKE.anon.do-not-use")
    SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "FAKE.service_role.do-not-use")

    # Used for the "summarise this lead" feature
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "sk-FAKE-doNotUse-000000000000000000000000")
