from django.db import models


class Entity(models.Model):

    """代表现实生活某一个实体"""

    name = models.CharField("name", max_length=20)
    descript = models.CharField("descript", max_length=100, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "物品"
        verbose_name_plural = "物品"
