from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from shortener.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path(
        "url-shortener/",
        include(
            ("shortener.urlshortener.urls", "shortener.urlshortener"),
            namespace="urlshortener"
        )
    )
]
