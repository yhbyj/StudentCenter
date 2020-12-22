from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from records.views import home_page
from records.models import Record


class HomePageTest(TestCase):

    def test_can_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class RecordModelTest(TestCase):

    def test_saving_and_retrieving_records(self):
        first_record = Record()
        first_record.text = '第一条记录'
        first_record.save()

        second_record = Record()
        second_record.text = '第二条记录'
        second_record.save()

        saved_records = Record.objects.all()
        self.assertEqual(saved_records.count(), 2)

        first_saved_record = saved_records[0]
        second_saved_record = saved_records[1]
        self.assertEqual(first_saved_record.text, '第一条记录')
        self.assertEqual(second_saved_record.text, '第二条记录')


class PackViewTest(TestCase):

    def test_can_use_pack_template(self):
        response = self.client.get(
            '/packs/the-only-record-in-the-world/'
        )

        self.assertTemplateUsed(response, 'pack.html')

    def test_can_display_all_saved_records(self):
        Record.objects.create(text='记录1')
        Record.objects.create(text='记录2')

        response = self.client.get(
            '/packs/the-only-record-in-the-world/'
        )

        self.assertContains(response, '记录1')
        self.assertContains(response, '记录2')


class NewPackTest(TestCase):

    def test_can_POST_a_request_and_save_record(self):
        response = self.client.post(
            '/packs/new',
            data={'record_text': '一条新的成长记录'}
        )

        self.assertEqual(Record.objects.count(), 1)
        new_record = Record.objects.first()
        self.assertEqual(new_record.text, '一条新的成长记录')

    def test_can_redirect_after_POST(self):
        response = self.client.post(
            '/packs/new',
            data={'record_text': '一条新的成长记录'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            '/packs/the-only-record-in-the-world/'
        )
