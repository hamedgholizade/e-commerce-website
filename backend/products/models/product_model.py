from django.db import models
from django.utils.text import slugify

from base.models import BaseModel
from products.models import Category


class Product(BaseModel):
    """
    Model to store product information.
    """
    PRODUCT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    brand = models.CharField(max_length=100)
    status = models.CharField(
        max_length=8,
        choices=PRODUCT_STATUS_CHOICES,
        default='draft',
    )
    category = models.ManyToManyField(
        Category,
        related_name='products'
    )

    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug from title."""
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

