import os
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_urls():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
                SELECT DISTINCT ON (urls.id)
                        urls.id AS id,
                        urls.name AS name,
                        url_checks.created_at AS last_check,
                        url_checks.status_code AS status_code
                    FROM urls
                    LEFT JOIN url_checks ON urls.id = url_checks.url_id
                    AND url_checks.id = (SELECT MAX(id)
                                        FROM url_checks
                                        WHERE url_id = urls.id)
                    ORDER BY urls.id DESC
            """
        )
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
        cursor.execute(
            f"""
                INSERT INTO urls (name, created_at)
                VALUES ('{name}', NOW())
            """
        )
        conn.commit()


def add_url_check(check):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(
            f"""
                INSERT INTO url_checks (url_id, status_code, created_at)
                VALUES ({check['url_id']}, {check['status_code']}, NOW())
            """
        )
        conn.commit()


def get_checks_by_url_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            f"""
                SELECT * FROM url_checks
                WHERE url_id = {id}
                ORDER BY id DESC
            """
        )
        return cursor.fetchall()
