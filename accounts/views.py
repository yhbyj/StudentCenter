from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import MyUser
from functional_tests.test_aaa import SUBJECT


def new_account(request):
    email = request.POST['email']
    user = MyUser(email=email)
    user.save()
    # print(type(send_mail))
    # 邮件发送方必须和登录用户一致
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject=SUBJECT,
        message='欢迎您！',
        from_email=from_email,
        recipient_list=[email]
    )
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

