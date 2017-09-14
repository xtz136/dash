"""dash URL Configuration """
from django.conf.urls import url, include
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from django.conf import settings

urlpatterns = [
    url(r'^crm/', include('crm.urls', namespace="crm")),
    url(r'^admin/', admin.site.urls),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^export_action/',
        include("export_action.urls", namespace="export_action")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
