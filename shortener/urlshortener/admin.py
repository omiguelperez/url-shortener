from django.contrib import admin

from shortener.urlshortener.models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("url", "shortened", "title", "views")
