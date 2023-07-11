from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('order', views.order, name="order"),
    path('order/detail', views.order_detail, name="order-detail"),
    path('order/open', views.open_orders, name="open-orders"),
    path('order/open/<int:id>', views.open_order_detail, name="open-order-detatil"),
]