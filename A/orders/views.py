from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product
from .forms import CartQuantityForm
from .cart import Cart
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'carts': cart})


class AddCartView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartQuantityForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')


class DeleteCartView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.delete(product)
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order})


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order_queryset = Order.objects.filter(user=request.user).exists()
        if order_queryset:
            order = Order.objects.get(user=request.user)
            messages.error(request, 'you have unpaid order! Please pay it first', 'danger')
        else:
            order = Order.objects.create(user=request.user)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['Price'],
                                         quantity=item['quantity'])
            # cart.clear()  # Whenever you config the ZarinPal pay system, you must uncomment this.
        return redirect('orders:order_detail', order.id)
