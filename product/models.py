from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from account.models import User
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
        ('True', True),
        ('False', False),
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    slug = models.SlugField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.SmallIntegerField(default=1)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=5, choices=STATUS, default='FALSE')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    # rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    # num_reviews = models.SmallIntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.image:
            return mark_safe(
                    '<img src="%s" height="50" width="50">' % self.image.url)
        return "No image found"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    title = models.CharField(max_length=100)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/')

    def __str__(self):
        return self.title
