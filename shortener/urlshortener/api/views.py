from django.conf import settings

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView

from shortener.urlshortener.api.serializers import (
    GenerateShortURLSerializer,
    ShortURLDetailSerializer,
    TopShortURLSerializer,
)
from shortener.urlshortener.models import ShortURL


class ShortURLView(CreateAPIView):
    serializer_class = GenerateShortURLSerializer
    queryset = ShortURL.objects.all()


generate_short_url_view = ShortURLView.as_view()


class ShortURLView(RetrieveAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLDetailSerializer
    lookup_field = 'short_url'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save()

        return obj


short_url_detail_view = ShortURLView.as_view()


class TopURLsView(ListAPIView):
    queryset = ShortURL.objects.order_by('-views')[:settings.TOP_N_URLS]
    serializer_class = TopShortURLSerializer


top_urls_view = TopURLsView.as_view()
