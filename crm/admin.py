from django.contrib import admin

from .models import Company, People, ShareHolder, Contract


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Contract)
class ContractModelAdmin(admin.ModelAdmin):
    pass


@admin.register(People)
class PeopleModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ShareHolder)
class ShareHolderModelAdmin(admin.ModelAdmin):
    pass
