from django.conf.urls import include, url
from rest_framework import routers
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'clients', views.CompanyViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'tags', views.TagViewSet)


urlpatterns = [
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^login/wechat/$', views.authorize, name='login_wechat'),
    url(r'^login/account/$', obtain_jwt_token, name='obtain_token'),
    url(r'^token/refresh/$', refresh_jwt_token, name='refresh_token'),
    url('^fields_info/$', views.FieldsInfoView.as_view(), name=''),
    url('^', include(router.urls)),
]
