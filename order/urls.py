from django.urls import path, include
from . import views
from .views import CreateOrderView


app_name = "order"

urlpatterns = [
    path('', views.scanner, name = 'home'),
    path('generate_qr', views.generate_qr, name = 'qr_code'),
    path('cafe/<int:cafe_id>/table/<int:table_id>/chair/<int:chair_id>/menu/',
         CreateOrderView.as_view(), name='menu'),
    path('order/<int:order_id>/confirm/', views.confirm, name="confirm_order"),  # placeholder
]



