from django.db import models
from django.shortcuts import reverse

from time import time

class News(models.Model):
    title = models.CharField(max_length=500)
    time = models.CharField(max_length=500)
    text = models.TextField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_body_url', kwargs={'slug': self.id})

    class Meta:
        ordering = ['-id']