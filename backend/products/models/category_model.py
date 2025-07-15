from django.db import models

from base.models import BaseModel


class Category(BaseModel):
    """
    Model to store product categories.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='media/categories/', default='media/categories/default.jpg'
    )
    parent = models.ForeignKey(
        'self', related_name='subcategories', on_delete=models.CASCADE, blank=True, null=True
    )
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

