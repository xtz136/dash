from django.db import models


class Industry(models.Model):
    name = models.CharField(name="行业名", max_length=200)