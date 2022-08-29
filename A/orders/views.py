from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product
from .forms import CartQuantityForm
from .cart import Cart


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        session = request.session['cart']
        ids = list(session.keys())
        result = [int(item) for item in ids]
        products = Product.objects.filter(id__in=result)
        for product in products:
            request.session['cart'][str(product.id)]['product_obj'] = product
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
    def get(self,request,product_id):
        cart=Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.delete(product)
        return redirect('orders:cart')
