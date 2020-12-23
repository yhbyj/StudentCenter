from django.db import models


class Record(models.Model):
    text = models.TextField(default='')
    pack = models.ForeignKey(
        'Pack',
        on_delete=models.CASCADE,
        default=None
    )


class Pack(models.Model):
    pass
