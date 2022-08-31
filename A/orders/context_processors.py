from .cart import Cart
from .models import Order
from django.shortcuts import get_object_or_404


def cart(request):
    return {
        'cart': Cart(request)
    }


def order(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user)
            return {
                'order': order
            }
        except Order.DoesNotExist:
            return {}
