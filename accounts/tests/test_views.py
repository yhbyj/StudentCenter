from unittest.mock import patch

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

    @patch('accounts.views.send_mail')
    def test_can_send_an_email_with_log_in_link(self, mock_send_mail):
        response = self.client.post(
            '/accounts/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(mock_send_mail.called, True)
        mock_send_mail.assert_called_with(
            subject=SUBJECT,
            message='欢迎您！',
            from_email='mock@example.com',
            recipient_list=[TEST_EMAIL]
        )

