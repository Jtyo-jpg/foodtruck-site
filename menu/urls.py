from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('order/', views.create_order, name='create_order'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]