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

    def get_database_uri(self):
        if self.DB_USER and self.DB_PASSWORD:
            return f"{self.DB_MOTOR}+{self.DB_CONNECTOR}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"
        else:
            return "sqlite:///db.sqlite3"
        
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.get_database_uri()