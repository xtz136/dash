from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^accounts/register/$',
        views.UserCreateView.as_view(),
        name='register'),
    url(r'^accounts/login/$',
        auth_views.LoginView.as_view(template_name='crm/login.html'),
        name='login'),
    url(r'^accounts/logout/$',
        auth_views.LogoutView.as_view(template_name='crm/logout.html'),
        name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^library/$', views.LibraryView.as_view(), name='library'),
    url(r'^customer/$', views.CustomerView.as_view(), name='customer'),
]
