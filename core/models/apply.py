from django.db import models
from django.conf import settings

from crm.models import Company

from django_fsm import FSMField, transition


class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200, blank=True)
    title = models.CharField('company title', max_length=200, blank=True)
    info = models.TextField(blank=True)
    phone = models.CharField('phone', max_length=50, blank=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    state = FSMField(default='new')

    @transition(field=state, source='new', target='approved')
    def approve(self):
        self.user.profile.company = self.company
        self.user.is_active = True
        self.user.save()
        # send notify

    @transition(field=state, source='new', target='denied')
    def deny(self):
        pass
        # send notify
