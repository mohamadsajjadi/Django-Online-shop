from django.db import models
from A.settings import AUTH_USER_MODEL
from home.models import Product


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name='order')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('paid', '-updated')

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.item.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity
