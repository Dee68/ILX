from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
# Create your models here.


User = get_user_model()


class WishList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wish List'

    def __str__(self):
        return f"{self.user.username}'s wishlist"
