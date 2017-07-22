from django.db import models

from .people import People
from .company import Company


class ShareHolder(models.Model):
    people = models.ForeignKey(People)
    company = models.ForeignKey(Company)

    ROLES = (
        ('legal', '法人'), ('share', '股东')
    )
    role = models.CharField(verbose_name="身份", choices=ROLES,
                            default="share", max_length=10)
    share = models.FloatField(verbose_name="占比", default=.1)

    people_name = models.CharField(max_length=200, editable=False, blank=True)
    company_title = models.CharField(
        max_length=255, editable=False, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.company_title, self.people_name)

    def save(self, *args, **kwargs):
        self.people_name = self.people.name
        self.company_title = self.company.title
        super(ShareHolder, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('people', 'company')
