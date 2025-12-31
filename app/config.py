import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:root@localhost:5432/personas_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
