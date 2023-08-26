from django.db import models
from product.models import Product
from django.conf import settings
# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user',
        blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product',
        blank=True,
        )

    class Meta:
        verbose_name_plural = 'Wish List'

    def __str__(self):
        return f"{self.user.username}'s wish list"
