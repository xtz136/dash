from django.db import models


class Industry(models.Model):
    name = models.CharField(verbose_name="行业名", max_length=200)

    def __str__(self):
        return self.name
