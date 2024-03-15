import re

import requests

from shortener.urlshortener.exceptions import CannotGetPageTitle, FailedToPullURLContent


def get_page_title(url: str) -> str:
    response = requests.get(url)

    if not response.ok:
        raise FailedToPullURLContent(f"Failed to pull content from {url}")

    content = str(response.content)
    regex = r"<title[^>]*>([^<]+)</title>"
    r = re.compile(regex)
    matches = r.search(content)
    if not matches:
        raise CannotGetPageTitle(f"Cannot get page title from {url}")
    page_title = matches.group(1)

    return page_title
