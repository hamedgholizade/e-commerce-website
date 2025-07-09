from django.db import models

from base.models import BaseModel
from products.models import Product



class ProductImage(BaseModel):
    """
    Model to store product images.
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/products' ,default='image/products/default.jpg')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"image for {self.product.title}"
 