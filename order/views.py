from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
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
    context = {'menu_list':menu_list, 'table':table, 'chair': chair}
    return render(request, "order/home.html", context)

def scanner(request):
    return render(request, "order/qrscanner.html")

import json

def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        return JsonResponse({"status":"success"})


