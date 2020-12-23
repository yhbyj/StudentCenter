from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.models import Record, Pack


def home_page(request):
    return render(request, 'home.html')


def view_pack(request):
    records = Record.objects.all()
    return render(request, 'pack.html', {'records': records})


def new_pack(request):
    pack = Pack.objects.create()
    Record.objects.create(
        text=request.POST['record_text'],
        pack=pack
    )
    return redirect('/packs/the-only-record-in-the-world/')
