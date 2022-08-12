from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
from .tasks import all_bucket_object_task


class HomeView(View):
    def get(self, request):
        product = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': product})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/product_detail.html', {'products': product})


class BucketHomeView(View):
    def get(self, request):
        objects = all_bucket_object_task()
        return render(request, 'home/bucket.html', {'objects': objects})
