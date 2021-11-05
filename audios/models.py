from django.db import models

class Audios(models.Model):
    text = models.TextField(default='no text entered')
    url = models.CharField(max_length=100)
    hint = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.text

