from accounts.models import Token, MyUser


class MyTokenAuthenticationBackend(object):

    def authenticate(self, request, uuid):
        try:
            token = Token.objects.get(uuid=uuid)
            return MyUser.objects.get(email=token.email)
        except Token.DoesNotExist:
            return None
        except MyUser.DoesNotExist:
            return MyUser.objects.create(email=token.email)

    def get_user(self, email):
        try:
            return MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return None
