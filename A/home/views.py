from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product


class HomeView(View):
    def get(self, request):
        product = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': product})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/product_detail.html', {'products': product})
