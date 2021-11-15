from django.db import models

class Audios(models.Model):
    from_tel = models.CharField(max_length=30, default='version1_default')
    text = models.TextField(default='no text entered')
    url = models.CharField(max_length=200)
    hint = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.text

