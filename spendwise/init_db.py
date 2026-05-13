#!/usr/bin/env python
"""
Database initialization script.
Supports both SQLite (local development) and PostgreSQL (production).
Run this once to create all tables.
"""

from app import create_app, db

app = create_app()

with app.app_context():
    db_url = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    db_type = "SQLite" if "sqlite" in db_url else "PostgreSQL"
    
    print(f"Initializing {db_type} database...")
    from app.models import user, expense, income  # noqa: F401
    db.create_all()
    print("✓ Database tables created successfully!")
    print(f"  Database: {db_type}")
    if "sqlite" in db_url:
        print("  Note: Using SQLite for local development.")
        print("  For production, set DATABASE_URL to a PostgreSQL connection string.")

