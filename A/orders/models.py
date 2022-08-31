from django.db import models
from A.settings import AUTH_USER_MODEL
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name='order')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount_amount = models.IntegerField(blank=True, null=True, default=False)

    class Meta:
        ordering = ('paid', '-updated')

    def get_total_cost(self):
        total_price = sum(item.get_cost() for item in self.item.all())
        if self.discount_amount:
            discount_amount = (total_price * self.discount_amount) // 100
            total_price -= discount_amount
            return int(total_price)
        else:
            return total_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    discount_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(90)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
