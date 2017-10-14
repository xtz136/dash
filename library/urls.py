from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^receive/$',
        views.ItemReceiveView.as_view(), name='item-receive'),
    url(r'^borrow/$',
        views.ItemBorrowView.as_view(), name='item-borrow'),
    url(r'^items/$',
        views.ItemListView.as_view(), name='item-list'),
    url(r'^receipt/$',
        views.ReceiptListView.as_view(), name='receipt-list'),
    url(r'^receipt/(?P<pk>\d+)/$',
        views.ReceiptDetailView.as_view(), name='receipt-detail'),
]
