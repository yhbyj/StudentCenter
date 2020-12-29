from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.forms import RecordForm, EMPTY_RECORD_ERROR
from records.models import Record, Pack


def home_page(request):
    return render(
        request,
        'home.html',
        {'form': RecordForm()}
    )


def view_pack(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    form = RecordForm()
    if request.method == 'POST':
        form = RecordForm(data=request.POST)
        if form.is_valid():
            Record.objects.create(
                text=request.POST['text'],
                pack=pack
            )
            return redirect(pack)
    return render(
        request,
        'pack.html',
        {
            'pack': pack,
            'form': form
        }
    )


def new_pack(request):
    form = RecordForm(data=request.POST)
    if form.is_valid():
        pack = Pack.objects.create()
        Record.objects.create(
            text=request.POST['text'],
            pack=pack
        )
        return redirect(pack)
    else:
        return render(
            request,
            'home.html',
            {
                'form': form
            }
        )

