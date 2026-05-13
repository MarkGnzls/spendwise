import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    
    # Use PostgreSQL if DATABASE_URL is set, otherwise use SQLite for local development
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # SQLite for local development
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'spendwise.db')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
