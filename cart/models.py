from django.db import models
from django.contrib.auth.models import User

from products.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'User Cart'
        verbose_name_plural = 'User Carts'
        ordering = ('id',)


class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='c_products'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_products'
    )
    quantity = models.PositiveIntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.cart} - {self.product} - {self.quantity}'

    class Meta:
        verbose_name = 'Cart Product'
        verbose_name_plural = 'Cart Products'
        ordering = ('id',)

    def get_total(self):
        total = 0
        for _ in range(self.quantity):
            total += self.product.price
        return total
