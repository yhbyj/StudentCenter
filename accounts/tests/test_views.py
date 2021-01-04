from django.core import mail
from django.test import TestCase

from accounts.models import MyUser
from functional_tests.test_aaa import SUBJECT, TEST_EMAIL


class NewAccountTest(TestCase):

    def test_can_POST_a_request(self):
        response = self.client.post(
            '/accounts/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(response.status_code, 200)

    def test_can_POST_a_request_and_save_account(self):
        response = self.client.post(
            '/accounts/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(MyUser.objects.count(), 1)
        user = MyUser.objects.first()
        self.assertEqual(user.email, TEST_EMAIL)

    def test_can_send_an_email_with_log_in_link(self):
        pass
