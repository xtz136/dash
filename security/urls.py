from django.conf.urls import url

from .views import update_whitelist_view


urlpatterns = [
    url(r'^whitelist/$', update_whitelist_view, name='whitelist')
]
