from django.urls import path, include
from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHomeView.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', views.DeleteObjectBucketView.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', views.DownloadObjectBucketView.as_view(), name='download_obj_bucket'),
]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
