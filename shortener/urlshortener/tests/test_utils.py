from unittest.mock import Mock
from uuid import UUID

import pytest

from shortener.urlshortener.exceptions import CannotGetPageTitle, FailedToPullURLContent
from shortener.urlshortener.utils.crawler import get_page_title
from shortener.urlshortener.utils.shortener import get_shortest_url


class TestCrawlerUtils:

    @pytest.fixture
    def mock_get(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr("shortener.urlshortener.utils.crawler.requests.get", mock)
        yield mock

    def test_get_page_title(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = (
            b"<html><head><title>Test Wiki Page</title></head><body></body></html>"
        )
        url = "http://example.test"
        assert get_page_title(url) == "Test Wiki Page"

    def test_get_page_title_failed_to_pull_url_content(self, mock_get):
        mock_get.return_value.ok = False
        url = "http://example.test"
        with pytest.raises(FailedToPullURLContent) as exc_info:
            get_page_title(url)
        assert str(exc_info.value) == f"Failed to pull content from {url}"

    def test_cannot_get_page_title(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.content = b"<html><head></head><body></body></html>"
        url = "http://example.test"
        with pytest.raises(CannotGetPageTitle) as exc_info:
            get_page_title(url)
        assert str(exc_info.value) == f"Cannot get page title from {url}"


class TestGetPageTitle:
    @pytest.fixture
    def mock_uuid4(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr("shortener.urlshortener.utils.shortener.uuid4", mock)
        yield mock

    def test_get_page_title(self, mock_uuid4):
        mock_uuid4.return_value = UUID("6f3e8dae-dc5b-4971-8d76-0a5dbb598e1e")
        url = "http://example.test/hello-world-with-pytest"
        assert get_shortest_url(url) == "6f3e8dae-dc5b-4971-8d76-0a5dbb598e1e"
