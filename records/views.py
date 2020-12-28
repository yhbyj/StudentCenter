from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.models import Record, Pack


def home_page(request):
    return render(request, 'home.html')


def view_pack(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    records = Record.objects.filter(pack=pack)
    return render(
        request,
        'pack.html',
        {'pack': pack}
    )


def new_pack(request):
    pack = Pack.objects.create()
    record = Record(
        text=request.POST['record_text'],
        pack=pack
    )
    try:
        record.full_clean()
        record.save()
    except ValidationError:
        pack.delete()
        return render(
            request,
            'home.html',
            {'error': '你不能提交一条空的记录！'}
        )
    return redirect(f'/packs/{pack.id}/')


def add_item(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    Record.objects.create(
        text=request.POST['record_text'],
        pack=pack
    )
    return redirect(f'/packs/{pack.id}/')
