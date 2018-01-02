from django.db import models
from solo.models import SingletonModel


class SiteConf(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    site_address = models.CharField(blank=True, max_length=255)
    custom_css = models.CharField(blank=True, max_length=100)

    allow_custom_css = models.BooleanField(default=False)
    allow_sharefile = models.BooleanField(default=False)
    allow_preview = models.BooleanField(default=False)
    allow_like = models.BooleanField(default=False)
    allow_tag = models.BooleanField(default=False)

    site_log = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')
    site_favicon = models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/')

    # 集成
    # 微信相关
    enable_wechat = models.BooleanField(default=False)
    wx_appid = models.CharField(blank=True, max_length=255)
    wx_appsecret = models.CharField(blank=True, max_length=255)
    wx_redirect_uri = models.CharField(blank=True, max_length=255)
    wx_next_url = models.CharField(blank=True, max_length=255)

    # 微信通知模板
    wx_report_tpl = models.TextField('微信报表通知模板', blank=True)

    class Meta:
        verbose_name = "站点设置"
