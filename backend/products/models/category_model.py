from django.db import models
from django.utils.text import slugify

from base.models import BaseModel


class Category(BaseModel):
    """
    Model to store product categories.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', related_name='subcategories', on_delete=models.CASCADE, blank=True, null=True
    )
    
    class Meta:
        ordering = ['name']
        
    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug from name."""
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
