from django.core.exceptions import ValidationError
from django.db import IntegrityError
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

    def test_cannot_save_duplicate_records(self):
        pack = Pack.objects.create()
        Record.objects.create(text='dup', pack=pack)
        # with self.assertRaises(ValidationError):
        # IntegrityError 错误， 而不是 ValidationError 错误
        with self.assertRaises(IntegrityError):
            dup_record = Record(text='dup', pack=pack)
            # dup_record.full_clean()
            # Django 把 unique_together 约束添加到数据库中，而不是应用层
            # 所以要测 save 方法
            dup_record.save()

    def test_can_save_same_record_to_diffrent_pack(self):
        pack1 = Pack.objects.create()
        pack2 = Pack.objects.create()
        Record.objects.create(pack=pack1, text='dup')
        record = Record(pack=pack2, text='dup')
        record.full_clean()     # should not raise

    def test_pack_ordering(self):
        pack = Pack.objects.create()
        record1 = Record.objects.create(pack=pack, text='记录1')
        record2 = Record.objects.create(pack=pack, text='记录2')
        record3 = Record.objects.create(pack=pack, text='记录3')

        self.assertEqual(
            list(Record.objects.all()),
            [record1, record2, record3]
        )

    def test_string_representation(self):
        record = Record(text='成长记录')
        self.assertEqual(str(record), '成长记录')
