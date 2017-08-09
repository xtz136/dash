from django.conf.urls import include, url
from crm.views import import_model_view

urlpatterns = [
    url(r'^import/$', import_model_view, name='import-model-view'),
]
