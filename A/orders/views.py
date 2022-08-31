import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product
from .forms import CartQuantityForm, CouponCode
from .cart import Cart
from .models import Order, OrderItem, Coupon
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
    form_class = CouponCode

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order.html', {'order': order, 'form': self.form_class})


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


class CouponCodeView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = CouponCode(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, "we could not find this code or maybe this code has expired.", 'danger')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount_amount = coupon.discount_amount
            order.save()
        return redirect('orders:order_detail', order_id)
