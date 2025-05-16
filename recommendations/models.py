# models.py
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.JSONField(default=list)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
