from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
from django.conf import settings
from django.utils.safestring import mark_safe


class CategoryManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class Category(MPTTModel):
    STATUS = (
        ('True', True),
        ('False', False),
    )
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/category/'
        )
    slug = models.SlugField(max_length=200, unique=True)
    parent = TreeForeignKey(
            'self',
            blank=True,
            null=True,
            related_name='children',
            on_delete=models.CASCADE
                )
    status = models.CharField(max_length=5, choices=STATUS, default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
  
    class MPTTModel:
        order_insertion_by = ['title']

    objects = CategoryManager()
 
    def __str__(self):
        return str(self.title)


class Product(models.Model):
    STATUS = (
        (True, True),
        (False, False),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(blank=True, max_length=200)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.SmallIntegerField(default=1)
    photo1 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    photo3 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    photo4 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    photo5 = models.ImageField(upload_to='images/products/', blank=True, null=True)
    status = models.CharField(max_length=5, choices=STATUS, default=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    num_reviews = models.SmallIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class WishList(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         blank=True
#         )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True)

#     class Meta:
#         verbose_name_plural = "Wish List"

#     def __str__(self):
#         return f"{self.user.username}'s  wish list."
