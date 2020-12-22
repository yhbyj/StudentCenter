from django.db import models


class Record(models.Model):
    text = models.TextField(default='')
