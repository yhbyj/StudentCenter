import uuid
from django.test import TestCase

from accounts.authentication import MyTokenAuthenticationBackend
from accounts.models import Token, MyUser
from functional_tests.test_aaa import TEST_EMAIL


class AuthenticateTest(TestCase):

    def test_can_return_none_if_token_does_not_exist(self):
        _uuid = str(uuid.uuid4())
        user = MyTokenAuthenticationBackend().authenticate(
            self.client.request().wsgi_request,
            _uuid
        )
        self.assertIsNone(user)

    def test_can_return_user_if_token_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)
        _uuid = str(token.uuid)
        user = MyTokenAuthenticationBackend().authenticate(
            self.client.request().wsgi_request,
            _uuid
        )

        self.assertEqual(
            user,
            MyUser.objects.get(email=TEST_EMAIL)
        )


class GetUserTest(TestCase):

    def test_can_return_user_by_email(self):
        MyUser.objects.create(email=TEST_EMAIL)
        user = MyTokenAuthenticationBackend().get_user(
            TEST_EMAIL
        )

        self.assertEqual(
            user,
            MyUser.objects.get(email=TEST_EMAIL)
        )

    def test_can_return_none_if_user_does_not_exist_with_that_email(self):
        user = MyTokenAuthenticationBackend().get_user(
            TEST_EMAIL
        )
        self.assertIsNone(user)



