from django.db import transaction
from rest_framework import serializers

from shortener.urlshortener.models import ShortURL
from shortener.urlshortener.tasks import crawl_page_task
from shortener.urlshortener.utils.shortener import get_shortest_url


class GenerateShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ("url", "shortened")
        read_only_fields = ("shortened",)

    def save(self, **kwargs):
        url = self.validated_data["url"]

        self.context["shortened"] = get_shortest_url(url)
        short_url = ShortURL.objects.create(
            url=url,
            shortened=self.context["shortened"],
        )

        transaction.on_commit(lambda: crawl_page_task.delay(pk=short_url.id))

        return short_url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["shortened"] = self.context["shortened"]
        return data


class ShortURLDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ("url",)


class TopShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = (
            "title",
            "views",
        )
