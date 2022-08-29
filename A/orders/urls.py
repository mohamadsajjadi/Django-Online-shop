from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.AddCartView.as_view(), name='add_cart'),
    path('cart/delete/<int:product_id>/', views.DeleteCartView.as_view(), name='delete_cart')
]
