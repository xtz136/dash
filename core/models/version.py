from django.db import models


class Version(models.Model):
    version = models.CharField('version', max_length=100, blank=True)
    content = models.TextField(blank=True)
    created = models.DateTimeField(
        'created', auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.version

    def save(self, **kwargs):
        if not self.version:
            self.version = self.created.strftime('v%Y%m%d')
        super(Version, self).save(**kwargs)
