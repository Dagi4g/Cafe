from django.contrib import admin
from .models import Menu, Cafe, Chair , Table, Order, OrderItem

admin.site.register(Menu)
admin.site.register(Cafe)
admin.site.register(Chair)
admin.site.register(Table)

admin.site.register(Order)
admin.site.register(OrderItem)

