from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=5, default='en')
    title = models.CharField(max_length=48)
    original = models.CharField(max_length=48)
    image = models.ImageField(upload_to='flag/')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

class Rules(models.Model):
    rules = models.CharField(max_length=200)