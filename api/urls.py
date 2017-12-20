from django.conf.urls import include, url
from rest_framework import routers
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_extensions.routers import ExtendedSimpleRouter

# Routers provide an easy way of automatically determining the URL conf.
router = ExtendedSimpleRouter()
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)
router.register('company', views.CompanyViewSet)
router.register('projects', views.ProjectViewSet, base_name='project'
                ) .register('folders',
                            views.FolderViewSet,
                            base_name='projects-folder',
                            parents_query_lookups=['project'])

urlpatterns = [

    url(r'^upload/(?P<filename>.+)$',
        views.FileUploadView.as_view(), name='upload'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^login/wechat/$', views.authorize, name='login_wechat'),
    url(r'^login/account/$', obtain_jwt_token, name='obtain_token'),
    url(r'^token/refresh/$', refresh_jwt_token, name='refresh_token'),
    url('^fields_info/$', views.FieldsInfoView.as_view(), name=''),
    url('^', include(router.urls)),
]
