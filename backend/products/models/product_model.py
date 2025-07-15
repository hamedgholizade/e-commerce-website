from django.db import models
from django.utils.text import slugify

from base.models import BaseModel
from products.models import Category


class Product(BaseModel):
    """
    Model to store product information.
    """
    
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    stock = models.CharField(max_length=100, blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)
    category = models.ManyToManyField(
        Category,
        related_name='products'
    )

    def __str__(self):
        return self.name

