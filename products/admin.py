from django.contrib import admin
from . import models

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'price',
        'discount',
        'description',
        'condition',
        'seller',
        'delivery_type',
        'is_active',
        'created_on',
        'updated_on'
    )
    prepopulated_fields = {"slug": ("title",)}


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'rating',
        'product',
        'author',
        'created_on',
        'updated_on'
    )


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductReview, ProductReviewAdmin)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductQuestion)
admin.site.register(models.DeliveryType)
admin.site.register(models.Tag)
admin.site.register(models.Wishlist)
admin.site.register(models.Coupon)
admin.site.register(models.BrowsingHistory)
