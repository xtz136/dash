from django.db import models
from .company import Company


class Department(models.Model):

    title = models.CharField(verbose_name='部门名称',
                             blank=True,
                             max_length=200)
    company = models.ForeignKey(Company)
    parent = models.ForeignKey(
        "self", verbose_name="父级部门", blank=True, null=True)
    company_title = models.CharField(verbose_name='公司抬头',
                                     blank=True,
                                     editable=False,
                                     max_length=200)

    def __str__(self):
        return "{0} - {1}".format(self.company_title, self.title)

    def save(self, *args, **kwargs):
        self.company_title = self.company.title
        super(Department, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'
