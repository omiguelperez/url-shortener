from celery import shared_task

from shortener.urlshortener.models import ShortURL
from shortener.urlshortener.utils.crawler import get_page_title


@shared_task(name="crawl_page_task")
def crawl_page_task(pk: int):
    short_url = ShortURL.objects.get(pk=pk)  # raises ShortURL.DoesNotExist

    page_title = get_page_title(short_url.url)

    short_url.title = page_title
    short_url.save()

    return f"Page title: {page_title}"
