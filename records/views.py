from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from records.models import Record, Pack


def home_page(request):
    return render(request, 'home.html')


def view_pack(request, pack_id):
    pack = Pack.objects.get(id=pack_id)
    error = None
    if request.method == 'POST':
        try:
            record = Record(
                text=request.POST['record_text'],
                pack=pack
            )
            record.full_clean()
            record.save()
            return redirect(f'/packs/{pack.id}/')
        except ValidationError:
            error = '你不能提交一条空的记录！'
    return render(
        request,
        'pack.html',
        {'pack': pack, 'error': error}
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

