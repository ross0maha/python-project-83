import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_secret_key() -> str:
    '''Get secret key from .env file'''
    return SECRET_KEY


def get_database_url() -> str:
    '''Get database url from .env file'''
    return DATABASE_URL
