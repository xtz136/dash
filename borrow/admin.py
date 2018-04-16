from django.contrib import admin
from admin_view_permission.admin import AdminViewPermissionModelAdmin
from .models import entity, entity_list, revert_list


@admin.register(entity.Entity)
class EntityAdminView(admin.ModelAdmin):
    list_display = ("name", "descript")
    search_fields = ("name", "descript")


@admin.register(entity_list.EntityList)
class EntityListsAdminView(AdminViewPermissionModelAdmin):
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


@admin.register(revert_list.RevertList)
class RevertListAdminView(AdminViewPermissionModelAdmin):
    list_display = ("order_id", "company", "revert_borrow_date")
    search_fields = ("order_id", "company", "revert_borrow_date")
