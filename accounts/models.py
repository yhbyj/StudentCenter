from django.db import models


class MyUser(models.Model):
    email = models.EmailField(
        primary_key=True
    )
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True
