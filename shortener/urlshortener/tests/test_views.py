from uuid import UUID, uuid4

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from shortener.urlshortener.models import ShortURL
from shortener.users.models import User


@pytest.mark.django_db
class TestGenerateShortURlView:

    @pytest.fixture
    def api_client(self):
        user = User.objects.create_superuser(username="test", password="secret")
        token, _ = Token.objects.get_or_create(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        yield client

    def test_generate_short_url(self, api_client):
        url = "/api/url-shortener/generate/"
        payload = {"url": "https://en.wikipedia.org/wiki/Genghis_Khan"}
        response = api_client.post(url, payload)
        assert response.status_code == 201
        assert UUID(response.data["shortened"])

    def test_get_origination_url(self, api_client):
        shortened_url = ShortURL.objects.create(
            url="https://en.wikipedia.org/wiki", shortened=str(uuid4())
        )
        url = f"/api/url-shortener/{shortened_url.shortened}/"
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == {"url": "https://en.wikipedia.org/wiki"}

    def test_top_urls(self, api_client):
        ShortURL.objects.create(
            url="https://en.wikipedia.org/wiki",
            shortened=str(uuid4()),
            views=10,
            title="page-1",
        )
        ShortURL.objects.create(
            url="https://github.com/omiguelperez/url-shortener",
            shortened=str(uuid4()),
            views=200,
            title="page-2",
        )

        url = "/api/url-shortener/top/"
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.json() == [
            {"title": "page-2", "views": 200},
            {"title": "page-1", "views": 10},
        ]
