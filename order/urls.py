from django.urls import path, include
from . import views


app_name = "order"


urlpatterns = [
        path('', views.scanner, name = 'home'),
        path('menu' , views.menu, name= 'menu'),
        path('generate_qr', views.generate_qr, name = 'qr_code'),
        path('api/create-order/' ,views.create_order, name = 'create_order')
        ]


