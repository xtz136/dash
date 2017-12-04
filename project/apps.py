from django.apps import AppConfig
from django.db import models
from django.db.models.signals import class_prepared


class ProjectConfig(AppConfig):
    name = 'project'

    def ready(self):
        from actstream import registry
        registry.register('auth.User', 'project.Project')
