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
        ordering = ('id', )
        unique_together = ('pack', 'text')

    def __str__(self):
        return self.text


class Pack(models.Model):

    def get_absolute_url(self):
        return reverse('view_pack', args=[self.id])
