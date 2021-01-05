import re

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests import FunctionalTest


TEST_EMAIL = 'zhangsan@example.com'
SUBJECT = '您的登录链接'


class AuthenticationTest(FunctionalTest):

    def test_submit_an_email_address(self):
        # 张三发现首页的导航栏中有一个提交电子邮箱地址的输入框
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_name('email')

        self.assertEqual(
            input_box.get_attribute('placeholder'),
            '请输入您的电子邮箱地址'
        )

        # 在输入框中，他输入一个自己的电子邮箱地址，并提交
        input_box.send_keys(TEST_EMAIL)
        input_box.send_keys(Keys.ENTER)

        # 提交之后，他发现一条包含当前电子邮箱地址的提示信息
        self.wait_for(
            lambda: self.assertIn(
                TEST_EMAIL,
                self.browser.find_element_by_tag_name('body').text
            )
        )

    def test_can_log_in_with_an_email_link(self):
        # 张三在首页导航栏的输入框中输入了一个自己的电子邮箱地址
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_name('email')
        input_box.send_keys(TEST_EMAIL)
        input_box.send_keys(Keys.ENTER)

        # 提交之后，他根据返回的提示信息，
        # 检查自己的电子邮箱，发现一条新收到的信息
        self.wait_for(
            lambda: self.assertIn(
                TEST_EMAIL,
                self.browser.find_element_by_tag_name('body').text
            )
        )
        # 注意：一定要在看到返回的提示信息后，再检查自己的电子邮箱
        # 否则会出现“IndexError: list index out of range” 的错误
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # 打开这封电子邮件，他发现里面包含登录网站的链接
        url_search = re.search(
            r'http://.+/.+$',
            email.body
        )
        if not url_search:
            self.fail(
                f'在电子邮件中没有发现登录链接：\n{email.body}'
            )
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # 他试着点击该链接
        self.browser.get(url)

        # 居然登录成功了，他很开心
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(
                '登出'
            )
        )
        navbar = self.browser.find_element_by_css_selector(
            '.navbar'
        )
        self.assertIn(TEST_EMAIL, navbar.text)
