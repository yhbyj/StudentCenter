from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from accounts.models import MyUser, Token
from functional_tests.test_aaa import SUBJECT, TEST_EMAIL


class NewTokenViewTest(TestCase):

    def test_can_POST_a_request(self):
        response = self.client.post(
            '/accounts/tokens/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(response.status_code, 200)

    def test_can_POST_a_request_and_save_a_token(self):
        response = self.client.post(
            '/accounts/tokens/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(Token.objects.count(), 1)
        token = Token.objects.first()
        self.assertEqual(token.email, TEST_EMAIL)

    @patch('accounts.views.send_mail')
    def test_can_send_an_email_with_log_in_link(self, mock_send_mail):
        response = self.client.post(
            '/accounts/tokens/new',
            data={'email': TEST_EMAIL}
        )

        self.assertEqual(mock_send_mail.called, True)
        from_email = settings.EMAIL_HOST_USER
        mock_send_mail.assert_called_with(
            subject=SUBJECT,
            message='欢迎您！',
            from_email=from_email,
            recipient_list=[TEST_EMAIL]
        )

