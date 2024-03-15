from django.urls import path

from shortener.urlshortener.api.views import (
    generate_short_url_view,
    get_shortened_url_view,
    top_urls_view,
)

urlpatterns = [
    path("generate/", generate_short_url_view, name="generate"),
    path("top/", top_urls_view, name="top"),
    path("<shortened>/", get_shortened_url_view, name="get"),
]
