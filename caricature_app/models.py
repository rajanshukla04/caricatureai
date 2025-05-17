from django.db import models

from django.db import models

class StyleImage(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name