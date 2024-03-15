from django.db import models


class ShortURL(models.Model):
    url = models.URLField(max_length=500)
    shortened = models.CharField(max_length=150)
    title = models.TextField()
    views = models.PositiveIntegerField(default=0)

    def view(self):
        self.views += 1
