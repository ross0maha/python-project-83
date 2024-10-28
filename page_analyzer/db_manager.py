import psycopg2
from psycopg2.extras import RealDictCursor
from page_analyzer.env_manager import get_database_url


def db_connect() -> object:
    """Connect to db"""
    conn = psycopg2.connect(get_database_url())
    return conn


def get_urls() -> list:
    """Get all urls from db"""
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
    conn = db_connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request)
        return cursor.fetchall()


def get_urls_by_id(id: int) -> dict:
    """Get url by id"""
    request = "SELECT * FROM urls WHERE id = %s"

    conn = db_connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (id,))
        return cursor.fetchone()


def get_urls_by_name(name: str) -> dict:
    """Get url by name"""
    request = "SELECT * FROM urls WHERE name = %s"

    conn = db_connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (name,))
        return cursor.fetchone()


def add_url(name: str) -> None:
    """Add url to db"""
    request = """
                INSERT INTO urls (name, created_at)
                VALUES (%s, NOW())
            """
    conn = db_connect()
    with conn.cursor() as cursor:
        cursor.execute(request, (name,))
        conn.commit()


def add_url_check(url_data: dict) -> None:
    """Add url check to db"""
    conn = db_connect()
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
                url_data["url_id"],
                url_data["status_code"],
                url_data["h1"],
                url_data["title"],
                url_data["description"],
            ),
        )
        conn.commit()


def get_checks_by_url_id(id: int) -> list:
    """Get checks by url id"""
    request = """
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            """
    conn = db_connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(request, (id,))
        return cursor.fetchall()
