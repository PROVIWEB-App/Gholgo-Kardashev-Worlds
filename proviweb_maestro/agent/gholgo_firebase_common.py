# -*- coding: utf-8 -*-
"""Environment-driven Firebase Admin adapter (zero embedded credentials)."""

import os

DATABASE_URL = os.environ.get("FIREBASE_DATABASE_URL", "").strip()
ADMIN_CREDENTIALS_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()


def init_firebase_admin():
    """Initialize Firebase Admin SDK only when explicit env credentials exist."""
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if not creds_path or not os.path.exists(creds_path):
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials, db

        if not firebase_admin._apps:
            cred = credentials.Certificate(creds_path)
            opts = {"databaseURL": DATABASE_URL} if DATABASE_URL else {}
            firebase_admin.initialize_app(cred, opts)
        return db
    except Exception:
        return None
