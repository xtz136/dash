"""dash URL Configuration """
from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from django.contrib import admin
from django.conf import settings
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

    url(r'^borrow/', include('borrow.urls')),
    url(r'^index/', RedirectView.as_view(url='/borrow/')),

    url(r'^', include('borrow.urls', namespace="borrow")),
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
