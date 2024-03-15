from django.urls import path

from shortener.urlshortener.api.views import (
    generate_short_url_view,
    short_url_detail_view,
    top_urls_view,
)

urlpatterns = [
    path('generate/', generate_short_url_view, name="generate_short_url"),
    path('top/', top_urls_view, name="top_views"),
    path('<short_url>/', short_url_detail_view, name="detail"),
]
