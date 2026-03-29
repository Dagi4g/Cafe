from django.urls import path, include
from . import views


app_name = "order"


urlpatterns = [
        path('', views.scanner, name = 'home'),
        path('menu' , views.menu, name= 'menu'),
        path('generate_qr', views.generate_qr, name = 'qr_code'),
        path('create_order/<int:cafe_id>/<int:table_id>/<int:chair_id>/' ,views.create_order, name = 'create_order')
        ]


