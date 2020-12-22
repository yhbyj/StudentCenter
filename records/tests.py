from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from records.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.strip().startswith('<html>'))
        self.assertIn('<title>成长记录</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_post_a_request_and_return_correct_html(self):
        response = self.client.post(
            '/',
            data={'record_text': '一条新的成长记录'}
        )
        self.assertIn('一条新的成长记录', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
