from django.db import models
from django.db.models.signals import post_save

from .company import Company


class ShareHolder(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name="姓名")
    sfz = models.CharField(max_length=255, blank=True, verbose_name="身份证")
    company = models.ForeignKey(Company, verbose_name="公司")

    ROLES = [('法人', '法人'), ('股东', '股东'), ('员工', '员工')]
    role = models.CharField(verbose_name="职位",
                            choices=ROLES,
                            default="股东",
                            max_length=10)
    share = models.FloatField(verbose_name="股份占比%", default=.1)
    is_contactor = models.BooleanField(default=False,
                                       verbose_name="主要联系人")

    phone = models.CharField(verbose_name="电话",
                             blank=True, max_length=200)
    info = models.TextField(verbose_name="备注", blank=True)
    company_title = models.CharField(
        verbose_name='公司名',
        max_length=255, editable=False, blank=True)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.company_title, self.role, self.name)

    def save(self, *args, **kwargs):
        self.company_title = self.company.title
        super(ShareHolder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "股份持有人"
        verbose_name_plural = "股份持有人"


def update_shareholder_info(sender, instance, created, raw, **kwargs):
    info = [
        {
            'role': obj.role,
            'phone': obj.phone,
            'name': obj.name,
            'share': obj.share,
            'info': obj.info,
            'is_contactor': obj.is_contactor,
        } for obj in sender.objects.filter(company=instance.company)]
    instance.company.shareholder_info = info or []
    instance.company.save()


post_save.connect(update_shareholder_info, sender=ShareHolder)
