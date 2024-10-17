import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_secret_key():
    return SECRET_KEY


def get_database_url():
    return DATABASE_URL
