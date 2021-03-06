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
        input_box = self.get_record_input_element()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            '输入一条成长记录'
        )

        # 他在文本框中，输入“早读时，因为声音响亮，得到老师的表扬。”
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')

        # 当他敲了回车键后，页面自动更新，页面中出现：
        # “1、早读时，因为声音响亮，得到老师的表扬。”
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他好奇这个网站能不能记住他所输入的记录。
        # 他继续在页面的文本框中输入第二条成长记录：
        # “中午读写唱时，因为迟到，受到班主任的批评。”
        input_box = self.get_record_input_element()
        input_box.send_keys('中午读写唱时，因为迟到，受到班主任的批评。')

        # 当他敲了回车键后，页面再次自动更新，
        # 页面中同时出现两条他输入的带编号的记录。
        input_box.send_keys(Keys.ENTER)
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
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        input_box.send_keys(Keys.ENTER)
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
        input_box = self.get_record_input_element()
        input_box.send_keys('晚自修时，我写了2000字的作文，非常开心！')
        input_box.send_keys(Keys.ENTER)
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
        input_box = self.get_record_input_element()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

        # 他开始一个新的记录包
        input_box.send_keys('测试中！')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、测试中！'
        )
        input_box = self.get_record_input_element()
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )


class InputValidationTest(FunctionalTest):

    def test_cannot_add_empty_records(self):
        # 张三访问首页时，偶然提交了空的记录。
        self.browser.get(self.live_server_url)
        self.get_record_input_element().send_keys(Keys.ENTER)

        # 浏览器接受了请求，但是没有加载 pack 页
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            )
        )
        # 他试着输入一些内容
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            )
        )

        # 成功提交了记录
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他故意再次输入空的记录
        self.get_record_input_element().send_keys(Keys.ENTER)
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:invalid'
            )
        )

        # 他再次试着输入一些内容
        input_box = self.get_record_input_element()
        input_box.send_keys('中午读写唱时，因为迟到，受到班主任的批评。')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector(
                '#id_text:valid'
            )
        )
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )
        self.wait_for_row_text_in_table(
            '2、中午读写唱时，因为迟到，受到班主任的批评。'
        )

    def test_cannot_submit_duplicate_records(self):
        # 张三访问首页时，输入和提交了一条成长记录。
        self.browser.get(self.live_server_url)
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 他偶然输入和提交了和上一条一样的成长记录
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        input_box.send_keys(Keys.ENTER)

        # 他看到一条错误信息
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                '你已经提交过此成长记录！'
            )
        )

    def test_different_users_can_submit_same_record(self):
        # 张三访问首页时，输入和提交了一条成长记录。
        self.browser.get(self.live_server_url)
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )

        # 现在有一个新的用户，李四（Si Li），也来访问该网站。
        # 我们使用一个新的会话，确保不出现包含在cookies里的张三的信息。
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 李四访问首页时，输入和提交了一条和张三一样的成长记录。
        self.browser.get(self.live_server_url)
        input_box = self.get_record_input_element()
        input_box.send_keys('早读时，因为声音响亮，得到老师的表扬。')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_text_in_table(
            '1、早读时，因为声音响亮，得到老师的表扬。'
        )






