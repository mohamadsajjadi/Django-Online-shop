from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from . import tasks
from utils import UserIsAdminMixin


class HomeView(View):
    def get(self, request):
        product = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': product})


class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/product_detail.html', {'products': product})


class BucketHomeView(UserIsAdminMixin, View):

    def get(self, request):
        objects = tasks.all_bucket_object_task()
        return render(request, 'home/bucket.html', {'objects': objects})


class DeleteObjectBucketView(UserIsAdminMixin, View):

    def get(self, request, key):
        tasks.delete_obj_bucket.delay(key)
        messages.success(request, 'the objects will be deleted soon!', 'info')
        return redirect('home:bucket')


class DownloadObjectBucketView(UserIsAdminMixin, View):

    def get(self, request, key):
        tasks.download_obj_bucket.delay(key)
        messages.success(request, 'your object will download soon', 'info')
        return redirect('home:bucket')
