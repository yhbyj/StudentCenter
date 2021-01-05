from unittest.mock import patch

import uuid
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

        token = Token.objects.first()
        kwargs = tuple(mock_send_mail.call_args)[1]
        from_email = settings.EMAIL_HOST_USER
        expected_url = f'http://testserver/accounts/tokens/{token.uuid}'

        self.assertEqual(mock_send_mail.called, True)
        self.assertEqual(SUBJECT, kwargs['subject'])
        self.assertEqual(from_email, kwargs['from_email'])
        self.assertIn(expected_url, kwargs['message'])
        self.assertIn(TEST_EMAIL, kwargs['recipient_list'])


class TokenUUIDViewTest(TestCase):

    def test_can_redirect_to_home_page(self):
        response = self.client.get(
            f'/accounts/tokens/{uuid.uuid4()}'
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/'
        )

    def test_can_log_in_by_token(self):
        # token = Token.objects.create(email=TEST_EMAIL)
        # response = self.client.get(
        #     f'/accounts/tokens/{token.uuid}'
        # )
        #
        # user = MyUser.objects.get(email=token.email)
        #
        # self.assertIsInstance(response.context['user'], user)
        pass

