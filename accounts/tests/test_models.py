from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from functional_tests.test_aaa import TEST_EMAIL

User = get_user_model()


class MyUserModelTest(TestCase):

    def test_can_create_a_valid_user_with_email_address_only(self):
        user = User(email=TEST_EMAIL)
        user.full_clean()   # should not raise

    def test_must_have_a_primary_key_with_email(self):
        user = User(email=TEST_EMAIL)
        self.assertEqual(user.pk, TEST_EMAIL)

