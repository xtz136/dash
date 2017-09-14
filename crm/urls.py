from django.conf.urls import include, url
from crm.views import (import_model_view,
                       borrow_view,
                       item_bulk_add_view,
                       item_receipt_view)

urlpatterns = [
    url(r'^import/$', import_model_view, name='import-model-view'),
    url(r'^borrow/$', borrow_view, name='item-borrow'),
    url(r'^item/bulk_add/$', item_bulk_add_view, name='item-bulk-add'),
    url(r'^item/receipt/$', item_receipt_view, name='item-receipt'),
]
