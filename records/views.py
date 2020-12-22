from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.models import Record


def home_page(request):
    if request.method == 'POST':
        Record.objects.create(text=request.POST['record_text'])
        return redirect('/packs/the-only-record-in-the-world/')
    return render(request, 'home.html')


def view_pack(request):
    records = Record.objects.all()
    return render(request, 'pack.html', {'records': records})
