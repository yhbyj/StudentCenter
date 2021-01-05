from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import MyUser, Token
from functional_tests.test_aaa import SUBJECT


def new_account(request):
    email = request.POST['email']
    user = MyUser(email=email)
    # 注意：save 方法和 objects.create() 方法有很大区别
    # 例如，数据库中已经存储了一个电子邮箱地址，
    # 如果再用这个地址，前者不会报错，后者会报如下错误
    # django.db.utils.IntegrityError:
    # UNIQUE constraint failed: accounts_myuser.email
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


def new_token(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    # 邮件发送方必须和登录用户一致
    from_email = settings.EMAIL_HOST_USER
    send_mail(
        subject=SUBJECT,
        message='欢迎您！',
        from_email=from_email,
        recipient_list=[email]
    )
    response = HttpResponse(token.email)
    return response

