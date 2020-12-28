from django.test import TestCase

from records.forms import RecordForm, EMPTY_RECORD_ERROR


class RecordFormTest(TestCase):

    def test_form_record_input_has_placeholder_and_css_classes(self):
        form = RecordForm()

        self.assertIn('placeholder="输入一条成长记录"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_record(self):
        form = RecordForm(data={'text': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_RECORD_ERROR]
        )


