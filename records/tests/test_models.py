from django.core.exceptions import ValidationError
from django.test import TestCase

from records.models import Pack, Record


class PackAndRecordModelTest(TestCase):

    def test_saving_and_retrieving_records(self):
        pack = Pack()
        pack.save()
        first_record = Record()
        first_record.text = '第一条记录'
        first_record.pack = pack
        first_record.save()

        second_record = Record()
        second_record.text = '第二条记录'
        second_record.pack = pack
        second_record.save()

        saved_records = Record.objects.all()
        self.assertEqual(saved_records.count(), 2)

        first_saved_record = saved_records[0]
        second_saved_record = saved_records[1]
        self.assertEqual(first_saved_record.text, '第一条记录')
        self.assertEqual(first_saved_record.pack, pack)
        self.assertEqual(second_saved_record.text, '第二条记录')
        self.assertEqual(second_saved_record.pack, pack)

    def test_cannot_save_empty_records(self):
        pack = Pack.objects.create()
        record = Record(pack=pack, text='')
        with self.assertRaises(ValidationError):
            record.save()
            record.full_clean()

    def test_get_absolute_url(self):
        pack = Pack.objects.create()
        self.assertEqual(
            pack.get_absolute_url(),
            f'/packs/{pack.id}/'
        )

