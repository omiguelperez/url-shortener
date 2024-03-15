import re
import requests
from celery import shared_task

from shortener.urlshortener.models import ShortURL
from shortener.urlshortener.exceptions import FailedToPullURLContent, CannotGetPageTitle


@shared_task(name="pull_content_from_url")
def pull_content_from_url(pk: int):
    short_url = ShortURL.objects.get(pk=pk)

    response = requests.get(short_url.url)

    if not response.ok:
        raise FailedToPullURLContent(f"Failed to pull content from {short_url.url}")

    # Extract Page Title
    content = str(response.content)
    regex = r'<title[^>]*>([^<]+)</title>'
    r = re.compile(regex)
    matches = r.search(content)
    if not matches:
        raise CannotGetPageTitle(f"Cannot get page title from {short_url.url}")
    page_title = matches.group(1)

    short_url.content = page_title
    short_url.save()

    return f"Page title: {page_title}"
