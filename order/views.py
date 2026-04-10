from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.db import  transaction

import json
import qrcode
from io import BytesIO
import uuid

from .models import Cafe, Table, Chair, Menu, Order, OrderItem
from .forms import OrderItemFormSet

def show_error(request, error_message=None, error_title=None, redirect_url=None):
    """Generic error page handler"""
    if not isinstance(error_message, str) or not isinstance(error_title, str):
        raise TypeError(f"Expected str, got {type(error_message).__name__} for error_message and {type(error_title).__name__} for error_title")

    context = {
        'error_message': error_message or 'An unexpected error occurred.',
        'error_title': error_title.title() or 'Oops! Something went wrong',
        'redirect_url': redirect_url,
    }
    return render(request, 'order/error.html', context)


       
class CreateOrderView(View):
    def get(self, request, cafe_id, table_id, chair_id):
        request.session["order_token"] = str(uuid.uuid4())
        print(request.session.session_key)

        
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
                    'paired_list': paired_list,  
                }

            
            return render(request, 'order/menu.html', context)
        else:
            return show_error(request,
                              error_title="Chair Unavialable",
                              error_message=f"chair {chair.chair_id} in table {chair.table.table_id} is currently occopied, ")

    @transaction.atomic
    def post(self, request, cafe_id, table_id, chair_id ):
        #avoid unnecessry conflicting posts.

        token = request.POST.get('order_token')
    
        session_token = request.session.get('order_token')
        

        if not token or token != session_token:
            return redirect('order:menu', cafe_id=cafe_id, table_id=table_id, chair_id=chair_id)
        # Invalidate token after use
        del request.session['order_token']


        cafe = get_object_or_404(Cafe, id=cafe_id)
        table = get_object_or_404(Table, id=table_id, cafe=cafe)
        chair = get_object_or_404(Chair, id=chair_id, table=table)
        if not chair.is_occupied:

            formset = OrderItemFormSet(request.POST)

            if formset.is_valid():
                valid_items = []

                for form in formset:
                    if  form.cleaned_data['quantity'] > 0:
                        valid_items.append(form)


                if not valid_items:
                    messages.error(request,"please select atleast one iteam.")
                    return redirect('order:menu', cafe_id=cafe.id, table_id=table.id, chair_id=chair.id )

                # Create Order
                order = Order.objects.create(
                    chair=chair,
                    status=Order.Status.PENDING
                )

                for form in valid_items:
                    item = form.save(commit=False)
                    item.order = order
                    item.save()
                chair.occupy()

                return redirect('order:confirm_order', order_id=order.id)

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
            return show_error(request,
                              error_title="Chair Unavialable",
                              error_message=f"chair {chair.chair_id} in table {chair.table.table_id} is currently occopied, ")



#need to download pilliow , that is why it isn't working know.
def generate_qr(request):
    url = f"http://127.0.0.1:8000/menu"
    qr = qrcode.make(url)
                
    response = HttpResponse(content_type="menu/jpg")
    qr.save(response, "JPG")
    return response

def scanner(request):
    return render(request, "order/qrscanner.html")

def confirm(request, order_id):
    order_items = OrderItem.objects.filter(order_id=order_id, order__status=Order.Status.PENDING)


    if not order_items.exists():
        # Handle empty order case
        return show_error(request,
                          error_title="No Iteam Found",
                          error_message="This order doesn't exist make an order.")


    if not order_items[0].order.is_expired:
        
        total = sum(item.total_price() for item in order_items)
        
        context = {
            "order": order_items,
            "total": total,
            "order_info": order_items.first().order  # Access order info safely
        }
        
        return render(request, "order/confirm_order.html", context)
    else :
        return show_error(request,
                          error_message="this order had expired, please make another order!",
                          error_title="Expired Order")
