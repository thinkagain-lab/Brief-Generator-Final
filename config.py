import os

class Config:
    SECRET_KEY = os.urandom(24)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///brief_generator.db'
    SQLALCHEMY_DATABASE_URI = "sqlite:///DATABASE_URL.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
