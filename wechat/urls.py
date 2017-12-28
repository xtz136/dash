from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url('^login/$', views.authorize, name='login'),
    url('^reports/$', login_required(views.ReportListView.as_view(),
                                     login_url='wechat:login'), name='report-list'),
    url('^$', login_required(views.index, login_url='wechat:login'), name='index'),
]
