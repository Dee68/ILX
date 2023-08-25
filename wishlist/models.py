from django.db import models
from product.models import Product
from django.conf import settings
# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    class Meta:
        verbose_name_plural = 'Wish List'

    def __str__(self):
        return f"{self.user.username}'s wish list"
