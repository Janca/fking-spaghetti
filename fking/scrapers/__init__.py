from fking.scrapers.gettyimages import GettyImages as _GettyImages
from fking.scrapers.imagescraper import IScraper as _IScraper

__all__ = [
    "get",
    "get_all"
]


def get_all() -> dict[str, _IScraper]:
    return {
        'Getty Images': _GettyImages()
    }


def get(key: str) -> _IScraper:
    scrapers = get_all()
    if key not in scrapers:
        raise ValueError(f"Invalid scraper id [{key}].")
    return scrapers[key]
