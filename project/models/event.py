from django.db import models


class Event(models.Model):
    type = models.CharField()
    user = models.ForeignKey
    content = models.CharField('')
    created = models.DateTimeField(auto_now_add=True)
