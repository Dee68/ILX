from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, ProductImage


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count',
                    'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_count',
                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 10


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller', 'location', 'category', 'image_tag']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
