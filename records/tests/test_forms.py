from django.test import TestCase

from records.forms import RecordForm, EMPTY_RECORD_ERROR, ExistingRecordForm, DUPLICATE_RECORD_ERROR
from records.models import Pack, Record


class RecordFormTest(TestCase):

    def test_form_record_input_has_correct_attributes(self):
        form = RecordForm()

        self.assertIn('name="text"', form.as_p())
        self.assertIn('placeholder="输入一条成长记录"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_record(self):
        form = RecordForm(data={'text': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_RECORD_ERROR]
        )

    def test_form_save(self):
        pack = Pack.objects.create()
        form = RecordForm(data={'text': '一条成长记录'})
        new_record = form.save(for_pack=pack)
        self.assertEqual(new_record, Record.objects.first())
        self.assertEqual(new_record.text, '一条成长记录')
        self.assertEqual(new_record.pack, pack)


class ExistingRecordFormTest(TestCase):

    def test_form_record_input_has_correct_attributes(self):
        pack = Pack.objects.create()
        form = ExistingRecordForm(for_pack=pack)

        self.assertIn('placeholder="输入一条成长记录"', form.as_p())

    def test_form_validation_for_blank_record(self):
        pack = Pack.objects.create()
        form = ExistingRecordForm(for_pack=pack, data={'text': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_RECORD_ERROR]
        )

    def test_form_save(self):
        pack = Pack.objects.create()
        form = ExistingRecordForm(for_pack=pack, data={'text': '一条成长记录'})
        new_record = form.save()
        self.assertEqual(new_record, Record.objects.first())
        self.assertEqual(new_record.text, '一条成长记录')
        self.assertEqual(new_record.pack, pack)

    def test_form_validation_for_duplicate_records(self):
        pack = Pack.objects.create()
        Record.objects.create(pack=pack, text='dup')
        form = ExistingRecordForm(for_pack=pack, data={'text': 'dup'})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_RECORD_ERROR]
        )



