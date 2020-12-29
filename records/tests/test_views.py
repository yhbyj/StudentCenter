from django.test import TestCase

from records.forms import RecordForm, EMPTY_RECORD_ERROR
from records.models import Pack, Record


class HomePageTest(TestCase):

    def test_can_use_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_can_pass_record_form(self):
        response = self.client.get('/')

        self.assertIsInstance(
            response.context['form'],
            RecordForm
        )


class PackViewTest(TestCase):

    def test_can_use_pack_template(self):
        pack = Pack.objects.create()
        response = self.client.get(
            f'/packs/{pack.id}/'
        )

        self.assertTemplateUsed(response, 'pack.html')

    def test_can_display_only_saved_records_for_that_pack(self):
        that_pack = Pack.objects.create()
        Record.objects.create(text='记录1', pack=that_pack)
        Record.objects.create(text='记录2', pack=that_pack)

        other_pack = Pack.objects.create()
        Record.objects.create(text='记录3', pack=other_pack)
        Record.objects.create(text='记录4', pack=other_pack)

        response = self.client.get(
            f'/packs/{that_pack.id}/'
        )

        self.assertContains(response, '记录1')
        self.assertContains(response, '记录2')
        self.assertNotContains(response, '记录3')
        self.assertNotContains(response, '记录4')

    def test_can_pass_a_pack_to_template(self):
        pack = Pack.objects.create()
        response = self.client.get(
            f'/packs/{pack.id}/'
        )

        self.assertEqual(response.context['pack'], pack)

    def test_can_pass_input_validation_errors(self):
        pack = Pack.objects.create()
        response = self.client.post(
            f'/packs/{pack.id}/',
            data={'text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pack.html')
        self.assertContains(response, EMPTY_RECORD_ERROR)

    def test_can_pass_record_form(self):
        pack = Pack.objects.create()
        response = self.client.get(
            f'/packs/{pack.id}/'
        )

        self.assertIsInstance(
            response.context['form'],
            RecordForm
        )
        self.assertContains(response, 'name="text"')

    def test_can_pass_duplicate_records_validation_errors(self):
        pack = Pack.objects.create()
        Record.objects.create(pack=pack, text='dup')
        response = self.client.post(
            f'/packs/{pack.id}/',
            data={'text': 'dup'}
        )

        self.assertEqual(Record.objects.count(), 1)
        self.assertTemplateUsed(response, 'pack.html')
        self.assertContains(response, '你已经提交过此成长记录！')

    def test_can_get_ordered_records(self):
        pack = Pack.objects.create()
        new_records = []
        for i in range(3):
            record = Record.objects.create(
                pack=pack,
                text=f'第{i+1}条成长记录'
            )
            new_records.append(record)

        response = self.client.get(
            f'/packs/{pack.id}/'
        )
        pack_records = response.context['pack'].record_set.all()

        self.assertEqual(len(new_records), len(pack_records))
        for i in range(len(pack_records)):
            self.assertEqual(
                new_records[i].text,
                pack_records[i].text
            )


class NewPackTest(TestCase):

    def test_can_POST_a_request_and_save_record(self):
        response = self.client.post(
            '/packs/new',
            data={'text': '一条新的成长记录'}
        )

        self.assertEqual(Record.objects.count(), 1)
        new_record = Record.objects.first()
        self.assertEqual(new_record.text, '一条新的成长记录')

    def test_can_redirect_after_POST(self):
        response = self.client.post(
            '/packs/new',
            data={'text': '一条新的成长记录'}
        )

        pack = Pack.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/packs/{pack.id}/'
        )

    def test_must_not_save_empty_records(self):
        response = self.client.post(
            '/packs/new',
            data={'text': ''}
        )

        self.assertEqual(Pack.objects.count(), 0)
        self.assertEqual(Record.objects.count(), 0)

    def test_can_use_home_template_when_record_is_invalid(self):
        response = self.client.post(
            '/packs/new',
            data={'text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_can_pass_validation_errors_when_record_is_invalid(self):
        response = self.client.post(
            '/packs/new',
            data={'text': ''}
        )

        self.assertContains(response, EMPTY_RECORD_ERROR)

    def test_can_pass_record_form_when_record_is_invalid(self):
        response = self.client.post(
            '/packs/new',
            data={'text': ''}
        )

        self.assertIsInstance(
            response.context['form'],
            RecordForm
        )


class NewRecordTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_pack(self):
        pack = Pack.objects.create()
        self.client.post(
            f'/packs/{pack.id}/',
            data={'text': '一条新的成长记录'}
        )

        self.assertEqual(Record.objects.count(), 1)
        record = Record.objects.first()
        self.assertEqual(record.pack, pack)
        self.assertEqual(record.text, '一条新的成长记录')

    def test_can_redirect_to_pack_view(self):
        pack = Pack.objects.create()
        response = self.client.post(
            f'/packs/{pack.id}/',
            data={'text': '一条新的成长记录'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/packs/{pack.id}/'
        )
