import validators
from urllib.parse import urlparse
from page_analyzer.db_manager import get_urls_by_name


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
    url_name = f'{url_parsed.scheme}://{url_parsed.netloc}'

    return {'error': error, 'url': url_name}