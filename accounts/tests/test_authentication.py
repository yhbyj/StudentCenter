import uuid
from django.test import TestCase

from accounts.authentication import MyTokenAuthenticationBackend
from accounts.models import Token, MyUser
from functional_tests.test_aaa import TEST_EMAIL


class AuthenticateTest(TestCase):

    def test_can_return_none_if_token_does_not_exist(self):
        user = MyTokenAuthenticationBackend().authenticate(
            self.client.request().wsgi_request,
            uuid.uuid4()
        )
        self.assertIsNone(user)

    def test_can_return_user_if_token_exists(self):
        token = Token.objects.create(email=TEST_EMAIL)
        user = MyTokenAuthenticationBackend().authenticate(
            self.client.request().wsgi_request,
            token.uuid
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



