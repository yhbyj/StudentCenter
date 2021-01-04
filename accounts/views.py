from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import MyUser


def new_account(request):
    user = MyUser(email=request.POST['email'])
    user.save()
    response = HttpResponse(user.email)
    return response
    # form = RecordForm(data=request.POST)
    # if form.is_valid():
    #     pack = Pack.objects.create()
    #     form.save(for_pack=pack)
    #     return redirect(pack)
    # else:
    #     return render(
    #         request,
    #         'home.html',
    #         {
    #             'form': form
    #         }
    #     )

