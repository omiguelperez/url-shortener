from rest_framework import serializers
from shortener.urlshortener.utils import get_short_url
from shortener.urlshortener.models import ShortURL
from shortener.urlshortener.tasks import pull_content_from_url


class GenerateShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ("url", "short_url")
        read_only_fields = ("short_url",)

    def validate(self, attrs):
        url = attrs["url"]
        # TODO: validations
        return attrs

    def save(self, **kwargs):
        url = self.validated_data["url"]

        self.context["short_url"] = get_short_url(url)
        short_url = ShortURL.objects.create(
            url=url,
            short_url=self.context["short_url"],
        )

        pull_content_from_url.delay(pk=short_url.id)

        return short_url

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["short_url"] = self.context["short_url"]
        return data


class ShortURLDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ("url",)


class TopShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ("content", "views",)
