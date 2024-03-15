from django.conf import settings

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from shortener.urlshortener.api.serializers import (
    GenerateShortURLSerializer,
    ShortURLDetailSerializer,
    TopShortURLSerializer,
)
from shortener.urlshortener.models import ShortURL


class GenerateShortURlView(CreateAPIView):
    serializer_class = GenerateShortURLSerializer
    queryset = ShortURL.objects.all()


generate_short_url_view = GenerateShortURlView.as_view()


class GetShortenedURLView(RetrieveAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLDetailSerializer
    lookup_field = 'shortened'

    def get_object(self):
        obj = super().get_object()
        obj.view()
        obj.save()

        return obj


get_shortened_url_view = GetShortenedURLView.as_view()


class TopURLsView(ListAPIView):
    queryset = ShortURL.objects.order_by('-views')[:settings.TOP_N_URLS]
    serializer_class = TopShortURLSerializer


top_urls_view = TopURLsView.as_view()
