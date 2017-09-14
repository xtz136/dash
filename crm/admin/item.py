from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from crm.models import Item, ItemBorrowingRecord


@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("company_title", "item", "note", "qty", "status",
                    "receiver",
                    "borrower",  "created", "return_date")
    search_fields = ("item", "company_title", "note")
    list_filter = ("item", "status")
    date_hierarchy = "created"
    raw_id_fields = ("company", )
    actions = ('borrow', "return_back", "gen_receipt")
    change_list_template = 'admin/crm/item_change_list.html'

    def borrow(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return redirect(reverse("crm:item-borrow") + "?ids={0}&ct={1}".format(
            ",".join(selected), ct.pk))
    borrow.short_description = "借出"

    def return_back(self, request, queryset):
        [o.return_back() for o in queryset]
    return_back.short_description = "归还物品给客户"

    def gen_receipt(self, request, queryset):
        [o.return_back() for o in queryset]
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return redirect(reverse("crm:item-receipt") + "?ids={0}".format(
            ",".join(selected)))
    gen_receipt.short_description = "生成收据"


@admin.register(ItemBorrowingRecord)
class ItemBorrowingRecordModelAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'borrower', 'reason',
                    'borrow_date', 'has_returned', 'status')
    list_filter = ('status', 'borrower')
