from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from accounts.models import Token
from functional_tests.test_aaa import TEST_EMAIL

User = get_user_model()


class MyUserModelTest(TestCase):

    def test_can_create_a_valid_user_with_email_address_only(self):
        user = User(email=TEST_EMAIL)
        user.full_clean()   # should not raise

    def test_must_have_a_primary_key_with_email(self):
        user = User(email=TEST_EMAIL)
        self.assertEqual(user.pk, TEST_EMAIL)


class TokenModelTest(TestCase):

    def test_can_create_a_valid_token_with_an_email_address(self):
        token1 = Token.objects.create(email=TEST_EMAIL)
        token2 = Token.objects.create(email=TEST_EMAIL)
        self.assertNotEqual(token1.uuid, token2.uuid)

