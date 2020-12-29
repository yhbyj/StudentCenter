from django.db import models
from django.urls import reverse


class Record(models.Model):
    text = models.TextField(default='')
    pack = models.ForeignKey(
        'Pack',
        on_delete=models.CASCADE,
        default=None
    )

    class Meta:
        unique_together = ('pack', 'text')


class Pack(models.Model):

    def get_absolute_url(self):
        return reverse('view_pack', args=[self.id])
