import psycopg2
from psycopg2.extras import RealDictCursor
from page_analyzer.env_manager import get_database_url


def get_urls():
    request = """
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
    conn = psycopg2.connect(get_database_url())
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request)
        return cursor.fetchall()


def get_urls_by_id(value):
    request = "SELECT * FROM urls WHERE id = %s"

    conn = psycopg2.connect(get_database_url())
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (value,))
        return cursor.fetchone()


def get_urls_by_name(value):
    request = "SELECT * FROM urls WHERE name = %s"

    conn = psycopg2.connect(get_database_url())
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (value,))
        return cursor.fetchone()


def add_url(name):
    request = """
                INSERT INTO urls (name, created_at)
                VALUES (%s, NOW())
            """
    conn = psycopg2.connect(get_database_url())
    with conn.cursor() as cursor:
        cursor.execute(request, (name,))
        conn.commit()


def add_url_check(check):
    conn = psycopg2.connect(get_database_url())
    request = """
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description,
                        created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """
    with conn.cursor() as cursor:
        cursor.execute(
            request,
            (
                check["url_id"],
                check["status_code"],
                check["h1"],
                check["title"],
                check["description"],
            ),
        )
        conn.commit()


def get_checks_by_url_id(id):
    request = """

                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            """
    conn = psycopg2.connect(get_database_url())
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (id,))
        return cursor.fetchall()
