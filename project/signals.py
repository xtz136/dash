import django.dispatch

project_added = django.dispatch.Signal(providing_args=['project', 'user'])
project_deleted = django.dispatch.Signal(providing_args=['project', 'user'])
