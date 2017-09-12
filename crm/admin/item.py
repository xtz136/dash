from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from crm.models import Item, ItemBorrowingRecord


@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("company_title", "item", "qty", "status",
                    "borrower",  "created", "return_date")
    search_fields = ("item", "company_title")
    list_filter = ("item", "status")
    raw_id_fields = ("company", )
    actions = ('borrow', )

    def borrow(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/crm/borrow/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    borrow.short_description = "借出"


@admin.register(ItemBorrowingRecord)
class ItemBorrowingRecordModelAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'borrower', 'reason',
                    'borrow_date', 'has_returned', 'status')
    list_filter = ('status', 'borrower')
