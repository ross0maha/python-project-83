import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM urls ORDER BY id DESC")
        return cursor.fetchall()


def get_urls_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"SELECT * FROM urls WHERE id = {id}")
        return cursor.fetchone()


def get_urls_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(f"SELECT * FROM urls WHERE name = '{name}'")
        return cursor.fetchone()


def add_url(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(f"INSERT INTO urls (name, created_at) VALUES ('{name}', NOW())")  # noqa E501
        conn.commit()


def add_check(check):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
            (check['url_id'],
             check['status_code'],
             check['h1'],
             check['title'],
             check['description'],
             check['checked_at']))
        conn.commit()
