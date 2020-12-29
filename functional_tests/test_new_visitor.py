from unittest import skip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from . import FunctionalTest


class InteractionTest(FunctionalTest):

    def test_can_start_a_pack_of_records_for_one_user(self):
        # 张三（San Zhang）听说一个记录成长经历的应用。
        # 他来查实该应用的首页。
        self.browser.get(self.live_server_url)

        # 他注意到页标题和头部包含“成长记录”信息。
        self.assertIn('成长记录', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('成长记录', header_text)

        # 他被邀请直接输入一条成长记录信息。
        inputbox = self.get_record_input_element()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '输入一条成长记录'
        )

        # 他在文本框中，输入“早读时，因为声音响亮，得到老师的表扬。”
        inputbox.send_keys('早读时，因为声音响亮，得到老师的表扬。')

        # 当他敲了回车键后，页面自动更新，页面中出现：
        # “1、早读时，因为声音响亮，得到老师的表扬。”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他好奇这个网站能不能记住他所输入的记录。
        # 他继续在页面的文本框中输入第二条成长记录：
        # “中午读写唱时，因为迟到，受到班主任的批评。”
        inputbox = self.get_record_input_element()
        inputbox.send_keys('中午读写唱时，因为迟到，受到班主任的批评。')

        # 当他敲了回车键后，页面再次自动更新，
        # 页面中同时出现两条他输入的带编号的记录。
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )
        self.wait_for_row_text_in_table(
            '2、中午读写唱时，因为迟到，受到班主任的批评。'
        )

        # 他心满意足，出去玩了！

    def test_multiple_users_can_start_packs_at_different_urls(self):
        # 张三（San Zhang）开始一个新的记录包（集）
        self.browser.get(self.live_server_url)
        inputbox = self.get_record_input_element()
        inputbox.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他发现该网站为他生成了一条唯一的URL地址。
        san_pack_url = self.browser.current_url
        self.assertRegex(san_pack_url, '/packs/.+')

        # 现在有一个新的用户，李四（Si Li），也来访问该网站。

        # 我们使用一个新的会话，确保不出现包含在cookies里的张三的信息。
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 李四访问首页。没有张三的记录包信息
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('早读时，因为声音响亮，得到老师的表扬。', page_text)
        self.assertNotIn('中午读写唱时，因为迟到，受到班主任的批评。', page_text)

        # 李四开始一个新的记录包
        inputbox = self.get_record_input_element()
        inputbox.send_keys('晚自修时，我写了2000字的作文，非常开心！')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、晚自修时，我写了2000字的作文，非常开心！'
        )

        # 李四也得到了一条唯一的URL地址。
        si_pack_url = self.browser.current_url
        self.assertRegex(si_pack_url, '/packs/.+')

        # 还是没有张三的记录包信息
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('早读时，因为声音响亮，得到老师的表扬。', page_text)
        self.assertNotIn('中午读写唱时，因为迟到，受到班主任的批评。', page_text)

        # 他们心满意足，出去玩了！


class CSSTest(FunctionalTest):
    @skip
    def test_layout_and_styling(self):
        # 张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 他注意到输入框是居中的
        inputbox = self.get_record_input_element()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 他开始一个新的记录包
        inputbox.send_keys('测试中！')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、测试中！'
        )
        inputbox = self.get_record_input_element()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )


class InputValidationTest(FunctionalTest):

    def test_cannot_add_empty_records(self):
        # 张三访问首页时，偶然提交了空的记录。
        self.browser.get(self.live_server_url)
        self.get_record_input_element().send_keys(Keys.ENTER)

        # 首页刷新后，出现一个错误提示“你不能提交一条空的记录！”
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                '你不能提交一条空的记录！'
            )
        )
        # 他试着输入一些内容，工作正常，错误消失
        inputbox = self.get_record_input_element()
        inputbox.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他故意再次输入空的记录
        self.get_record_input_element().send_keys(Keys.ENTER)

        # 在pack页，他再次收到相同的错误提示
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                '你不能提交一条空的记录！'
            )
        )

        # 他再次试着输入一些内容
        inputbox = self.get_record_input_element()
        inputbox.send_keys('中午读写唱时，因为迟到，受到班主任的批评。')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )
        self.wait_for_row_text_in_table(
            '2、中午读写唱时，因为迟到，受到班主任的批评。'
        )

        self.fail('测试通过！')



