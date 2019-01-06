from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import hack_export_action, views

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
    url(r'^client/batch/$',
        views.BatchClientUpdateView.as_view(),
        name='client-batch'),
    url(r'^client/search/$',
        views.ClientSearchView.as_view(),
        name='client-search'),
    url(r'^client/create/$',
        views.ClientCreateView.as_view(),
        name='client-create'),
    url(r'^client/(?P<pk>\d+)/$',
        views.ClientDetailView.as_view(),
        name='client-detail'),
    url(r'^client/(?P<pk>\d+)/edit/$',
        views.ClientEditView.as_view(),
        name='client-edit'),
]
