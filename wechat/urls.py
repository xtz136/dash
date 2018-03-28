from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url('^login/$', views.authorize, name='login'),

    url('^apply/success$',
        login_required(views.apply_success_view,
                       login_url='wechat:login'),
        name='apply-success'),

    url('^apply/$',
        login_required(views.ApplyCreateView.as_view(),
                       login_url='wechat:login'),
        name='apply-create'),

    url('^reports/$',
        login_required(views.ReportListView.as_view(),
                       login_url='wechat:login'),
        name='report-list'),

    url('^user/$',
        login_required(views.UserView.as_view(),
                       login_url='wechat:user'),
        name='user'),

    url('^$',
        login_required(views.index, login_url='wechat:login'),
        name='index'),
]
