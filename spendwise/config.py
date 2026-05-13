import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        database_url = database_url.replace("postgres://", "postgresql://")
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///spendwise.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False