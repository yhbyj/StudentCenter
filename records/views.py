from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.forms import RecordForm, EMPTY_RECORD_ERROR, ExistingRecordForm
from records.models import Record, Pack


def home_page(request):
    return render(
        request,
        'home.html',
        {'form': RecordForm()}
    )


def view_pack(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    form = ExistingRecordForm(for_pack=pack)
    if request.method == 'POST':
        form = ExistingRecordForm(for_pack=pack, data=request.POST)
        if form.is_valid():
            form.save()
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
        form.save(for_pack=pack)
        return redirect(pack)
    else:
        return render(
            request,
            'home.html',
            {
                'form': form
            }
        )

