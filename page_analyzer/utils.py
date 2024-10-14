import validators
import requests
from urllib.parse import urlparse
from page_analyzer.db_manager import get_urls_by
from bs4 import BeautifulSoup


def normalize_url(url):
    url_parsed = urlparse(url)
    url_name = f"{url_parsed.scheme}://{url_parsed.netloc}"
    return url_name


def validate_url(url):
    error = None
    url_name = normalize_url(url)

    match url_name:
        case url_name if len(url_name) > 255:
            error = "URL превышает 255 символов"
        case url_name if not validators.url(url_name):
            error = "Некорректный URL"
        case url_name if not url_name:
            error = "URL обязателен"
        case url_name if get_urls_by(url_name):
            error = "Страница уже существует"
    print({"error": error, "url": url_name})
    return {"error": error, "url": url_name}


def get_url_data(url):
    try:
        req = requests.get(url, timeout=10)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, "html.parser")
            h1_tag = soup.find("h1")
            title_tag = soup.find("title")
            description_tag = soup.find("meta", attrs={"name": "description"})

            check = {
                "status_code": req.status_code,
                "h1": h1_tag.text if h1_tag else "",
                "title": title_tag.text if title_tag else "",
                "description": (
                    description_tag.get("content") if description_tag else ""
                ),
            }

            return check
    except requests.RequestException:
        return None
