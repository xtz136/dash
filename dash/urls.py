"""dash URL Configuration """
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.views.generic import CreateView
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^export_action/',
        include("export_action.urls", namespace="export_action")),
    url('^inbox/notifications/',
        include('notifications.urls', namespace='notifications')),

    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^wechat/', include('wechat.urls', namespace='wechat')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^security/', include('security.urls', namespace="security")),
    url(r'^library/', include('library.urls', namespace="library")),
    url('^activity/', include('actstream.urls')),
<<<<<<< HEAD
=======

    url(r'^', include('crm.urls', namespace="crm")),
    url(r'^borrow/', include('borrow.urls')),
>>>>>>> 6c4dadf5af3db4df9f636d9e67838a7d9912009e
]

if settings.DEBUG:
    import debug_toolbar
    from django.views.static import serve
    urlpatterns += [

        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
