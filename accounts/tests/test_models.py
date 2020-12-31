from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):

    def test_can_create_a_valid_user_with_email_address_only(self):
        user = User(email='zhangsan@example.com')
        user.full_clean()   # should not raise
