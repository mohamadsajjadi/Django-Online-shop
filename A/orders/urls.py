from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.AddCartView.as_view(), name='add_cart'),
    path('cart/delete/<int:product_id>/', views.DeleteCartView.as_view(), name='delete_cart')
]
