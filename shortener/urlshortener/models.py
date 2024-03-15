from django.db import models


class ShortURL(models.Model):
    url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=150)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
