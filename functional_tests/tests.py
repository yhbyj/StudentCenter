import time

from django.test import LiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_text_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_table')
        rows = self.browser.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_record_list_and_retrieve_it_later(self):
        # 张三（San Zhang）听说一个记录成长经历的应用。
        # 他来查实该应用的首页。
        self.browser.get(self.live_server_url)

        # 他注意到页标题和头部包含“成长记录”信息。
        self.assertIn('成长记录', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('成长记录', header_text)

        # 他被邀请直接输入一条成长记录信息。
        inputbox = self.browser.find_element_by_id('id_new_record')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '输入一条成长记录'
        )

        # 他在文本框中，输入“早读时，因为声音响亮，得到老师的表扬。”
        inputbox.send_keys('早读时，因为声音响亮，得到老师的表扬。')

        # 当他敲了回车键后，页面自动更新，页面中出现：
        # “1、早读时，因为声音响亮，得到老师的表扬。”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他继续在页面的文本框中输入第二条成长记录：
        # “中午读写唱时，因为迟到，受到班主任的批评。”
        inputbox = self.browser.find_element_by_id('id_new_record')
        inputbox.send_keys('中午读写唱时，因为迟到，受到班主任的批评。')

        # 当他敲了回车键后，页面再次自动更新，
        # 页面中同时出现两条他输入的带编号的记录。
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )
        self.check_for_row_text_in_table(
            '2、中午读写唱时，因为迟到，受到班主任的批评。'
        )

        # 他好奇这个网站能不能记住他所输入的记录。
        # 他发现该网站为他生成了一条唯一的URL地址。
        self.fail('测试结束！')

        # 他访问了该URL地址。
        # 他录入的信息还在那儿。

        # 他心满意足，回去睡觉了。

