from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

import json
import qrcode
from io import BytesIO

from django.views import View
from .models import Cafe, Table, Chair, Menu, Order, OrderItem
from .forms import OrderItemFormSet

class CreateOrderView(View):
    def get(self, request, cafe_id, table_id, chair_id):
        cafe = get_object_or_404(Cafe, id=cafe_id)
        table = get_object_or_404(Table, id=table_id, cafe=cafe)
        chair = get_object_or_404(Chair, id=chair_id, table=table)

        if not chair.is_occupied:
            menu_items = Menu.objects.filter(cafe=cafe)
            initial_data = [{'food': item.id, 'quantity': 0, 'price': item.price} for item in menu_items]
            formset = OrderItemFormSet(initial=initial_data)

            # Build a paired list of (form, menu item)
            paired_list = list(zip(formset.forms, menu_items))
            context = {
                    'cafe': cafe,
                    'table': table,
                    'chair': chair,
                    'formset': formset,
                    'paired_list': paired_list,  # send this to template
                }

            
            return render(request, 'order/menu.html', context)
        else:
            return HttpResponse(f"{chair} is already occupied")

    def post(self, request, cafe_id, table_id, chair_id):
        cafe = get_object_or_404(Cafe, id=cafe_id)
        table = get_object_or_404(Table, id=table_id, cafe=cafe)
        chair = get_object_or_404(Chair, id=chair_id, table=table)
        if not chair.is_occupied:

            formset = OrderItemFormSet(request.POST)
            if formset.is_valid():
                # Filter out items with quantity = 0
                valid_items = [form for form in formset if form.cleaned_data['quantity'] > 0]

                if not valid_items:
                    return redirect('menu', cafe_id=cafe.id, table_id=table.id, chair_id=chair.id)

                # Create Order
                order = Order.objects.create(
                    chair=chair,
                    status='pending'
                )

                for form in valid_items:
                    item = form.save(commit=False)
                    item.order = order
                    item.save()
                chair.occupy()

                return redirect('confirm_order', order_id=order.id)

            # If formset invalid, reload menu
            menu_items = Menu.objects.filter(cafe=cafe)
            context = {
                'cafe': cafe,
                'table': table,
                'chair': chair,
                'formset': formset,
                'menu_items': menu_items,
            }
            paired_list = list(zip(formset.forms, menu_items))
            context['paired_list'] = paired_list
            return render(request, 'order/menu.html', context)
        else:
            return HttpResponse(f"{chair} is already occupied")



#need to download pilliow , that is why it isn't working know.
def generate_qr(request):
    url = f"http://127.0.0.1:8000/menu"
    qr = qrcode.make(url)
                
    response = HttpResponse(content_type="menu/jpg")
    qr.save(response, "JPG")
    return response

def scanner(request):
    return render(request, "order/qrscanner.html")

""""def confirm(request, order_id):
    order = """
    


