import validators
import requests
from urllib.parse import urlparse
from page_analyzer.db_manager import get_urls_by_name
from bs4 import BeautifulSoup


def validate_url(url):
    error = None
    url_parsed = None
    match url:
        case url if len(url) > 255:
            error = "URL превышает 255 символов"
        case url if not validators.url(url):
            error = "Некорректный URL"
        case url if not url:
            error = "URL обязателен"
        case url if get_urls_by_name(url):
            error = "Страница уже существует"

    url_parsed = urlparse(url)
    url_name = f"{url_parsed.scheme}://{url_parsed.netloc}"

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
