# Generated by Django 2.2 on 2020-12-31 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_auto_20201229_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ('id',)},
        ),
    ]
