from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG").lower() in ("true", "1") # type: ignore

    DB_MOTOR = os.getenv("DB_MOTOR")
    DB_CONNECTOR = os.getenv("DB_CONNECTOR")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    if DB_USER and DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f"{DB_MOTOR}+{DB_CONNECTOR}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"