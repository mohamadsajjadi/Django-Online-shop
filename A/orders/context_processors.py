from .cart import Cart
from .models import Order


def cart(request):
    return {'cart': Cart(request)}


# def order(request):
#     if request.user.is_authenticated:
#         try:
#             order = Order.objects.get(user=request.user)
#             return {
#                 'order', order
#             }
#         except Order.DoesNotExist:
#             return {}
