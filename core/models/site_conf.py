from django.db import models
from solo.models import SingletonModel


class SiteConf(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    site_address = models.BooleanField(default=False)
    custom_css = models.CharField(blank=True, max_length=100)

    allow_custom_css = models.BooleanField(default=False)
    allow_sharefile = models.BooleanField(default=False)
    allow_preview = models.BooleanField(default=False)
    allow_like = models.BooleanField(default=False)
    allow_tag = models.BooleanField(default=False)

    site_log = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')
    site_favicon = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')

    class Meta:
        verbose_name = "站点设置"
