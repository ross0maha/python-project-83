import validators
import requests
from urllib.parse import urlparse
import page_analyzer.db_manager as db
from bs4 import BeautifulSoup


TIMEOUT = 10  # timueout for http requests


def normalize_url(url) -> str:
    '''Normalize url to name'''
    url_parsed = urlparse(url)
    url_name = f"{url_parsed.scheme}://{url_parsed.netloc}"
    return url_name


def get_check(request) -> dict:
    '''
    Get check data from request
    status_code - http status code
    h1 - h1 tag text
    title - title tag text
    description - description tag content
    '''
    soup = BeautifulSoup(request.text, "html.parser")
    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    description_tag = soup.find("meta", attrs={"name": "description"})

    check = {
        "status_code": request.status_code,
        "h1": h1_tag.text if h1_tag else "",
        "title": title_tag.text if title_tag else "",
        "description": (
            description_tag.get("content") if description_tag else ""
        ),
    }

    return check


def validate_url(url_name) -> str:
    '''Validate url name and return errors'''
    error = None

    match url_name:
        case url_name if len(url_name) > 255:
            error = "size"
        case url_name if not validators.url(url_name):
            error = "incorrect_url"
        case url_name if not url_name:
            error = "empty_url"
        case url_name if db.get_urls_by_name(url_name):
            error = "exists"

    return error


def get_url_data(url) -> dict:
    '''Get url data from request'''
    try:
        request = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as error:
        return None

    if request.status_code == 200:
        check = get_check(request)
        return check
