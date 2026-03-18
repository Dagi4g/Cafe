from django.shortcuts import render
from django.http import HttpResponse
from .models import Menu

def index(request):
    menu_list = Menu.objects.all()
    context = {'menu_list':menu_list}
    return render(request, "order/home.html", context)
