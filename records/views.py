from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return HttpResponse('<html><title>成长记录</title></html>')
