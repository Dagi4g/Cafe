from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

import json
from . import models
import qrcode
from io import BytesIO

def generate_qr(request):
    url = f"http://127.0.0.1:8000/menu"
    qr = qrcode.make(url)
                
    response = HttpResponse(content_type="menu/jpg")
    qr.save(response, "JPG")
    return response

def menu(request):

    menu_list = models.Menu.objects.all()
    chair = models.Chair.objects.all()[0] # the first table from the query.
    table = chair.table
    cafe = table.cafe
    context = {'menu_list':menu_list, 'table':table, 'chair': chair, 'cafe' : cafe}
    return render(request, "order/home.html", context)

def scanner(request):
    return render(request, "order/qrscanner.html")


def create_order(request,cafe_id,table_id,chair_id):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        """cafe = get_object_or_404(models.Cafe,id=data['cafe_id'])
        table = get_object_or_404(models.Table,id=data['table_id'], cafe = cafe)
        chair = get_object_or_404(models.Chair,id=data['chair_id'], table=table)
        for items in data['items']:
            
            food = get_object_or_404(models.Menu, id=items["food_id"], cafe=cafe)
            if not chair.is_occupied:
                chair.occupy()
                order = models.Order.objects.create(item=food,chair=chair, cart=items["quantity"])

                print (chair.table)
                print(items['name'])
                print(order, order.total_price)
                context = {'order':order}
            else: 
                print(f"{chair} is occupied")"""

        return render(request, "order/home.html")



