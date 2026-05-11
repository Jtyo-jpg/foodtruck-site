from django.contrib import admin
from .models import Category, MenuItem, Customer, Order, OrderItem

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)