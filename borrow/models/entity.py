from django.db import models


class Entity(models.Model):

    """代表现实生活某一个实体"""

    name = models.CharField("entity name", max_length=20)
    descript = models.CharField("descript", max_length=100)
