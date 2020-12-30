from selenium.webdriver.common.keys import Keys

from functional_tests import FunctionalTest


class AuthenticationTest(FunctionalTest):

    def test_can_submit_an_email_address(self):
        # 张三发现首页有一个提交电子邮箱地址的输入框
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_name('email')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            '请输入您的电子邮箱地址'
        )

        # 在输入框中，他输入一个正确的电子邮箱地址
        # 例如“zhangsan@example.com”
        input_box.send_keys('zhangsan@example.com')

        # 提交之后，他发现一条包含当前电子邮箱地址的提示信息
        input_box.send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.assertContains(
                self.browser.find_element_by_tag_name('body').text,
                'zhangsan@example.com'
            )
        )

        # 他检查自己的电子邮箱，发现一条新收到的信息

        # 打开这封电子邮件，他发现里面包含登录网站的链接

        # 他试着点击该链接

        # 居然登录成功了，他很开心


        self.fail('测试成功')
