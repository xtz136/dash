from django.contrib import admin

from .models import entity, entity_list


@admin.register(entity.Entity)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("name", "descript")
    search_fields = ("name", "descript")


@admin.register(entity_list.EntityList)
class ReceiptModelAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "entity",
        'amount',
        'signer',
        'sign_date',
        'borrower',
        'borrow_date',
        'revert_borrow_date',
        'revert_date',
        'status',
        'descript')
    list_filter = (
        'status',
        'company',
        'entity',
        'signer',
        'borrower',
        'sign_date',
        'borrow_date')
    raw_id_fields = ('company', 'entity')
