import time
from enum import Enum

import bs4
import requests

import fking.legacy.proxies
import fking.legacy.queues
from fking.legacy.context import context

_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 " \
              "Safari/537.3"

default_headers = {'User-Agent': _user_agent}


class _ScrapeResult(Enum):
    COMPLETE = 1
    INCOMPLETE = 2
    ERROR = 3


def scrape_page_for_images(search_term: str, page_number):
    next_proxy = fking.legacy.proxies.next_best_proxy()

    try:
        url = __search_url(search_term, page_number)
        response = requests.get(url, headers=default_headers, proxies=next_proxy, timeout=5)
        if response.status_code != 200:
            return _ScrapeResult.ERROR

        document_html = response.text
        document_soup = bs4.BeautifulSoup(document_html, "html.parser")

        document_title = document_soup.find("h1")
        if document_title and document_title.text == "Oops! We can't find the page you are looking for.":
            return _ScrapeResult.COMPLETE

        gallery_images = document_soup.find_all("img", {"class": "MosaicAsset-module__thumb___yvFP5"})

        if gallery_images:
            for gallery_image in gallery_images:
                image_url = gallery_image["src"]
                image_alt_text = gallery_image["alt"]

                fking.legacy.queues.queue_image_download(search_term, image_url, image_alt_text)

        next_button_class = "PaginationRow-module__button___QQbMu PaginationRow-module__nextButton___gH3HZ"
        next_button = document_soup.find("button", {"class": next_button_class})

        if next_button:
            return _ScrapeResult.INCOMPLETE
        else:
            return _ScrapeResult.COMPLETE

    except:
        fking.legacy.proxies.mark_bad_proxy(next_proxy)
        return _ScrapeResult.ERROR


def scrape_search_term(search_term: str):
    current_page = 1
    attempts = 1

    while current_page <= context.max_pages and not context.interrupted:
        scrape_results = scrape_page_for_images(search_term, current_page)

        if scrape_results == _ScrapeResult.INCOMPLETE:
            current_page = current_page + 1
        elif scrape_results == _ScrapeResult.ERROR:
            if attempts <= context.max_attempts:
                continue
            else:
                break
        else:
            break


def __search_url(search_term: str, page_number: int) -> str:
    return f"https://www.gettyimages.com/photos/{search_term}" \
           f"?assettype=image" \
           f"&license=rf" \
           f"&alloweduse=availableforalluses" \
           f"&family=creative" \
           f"&phrase={search_term}" \
           f"&sort=mostpopular" \
           f"&numberofpeople=one" \
           f"&page={page_number}"
