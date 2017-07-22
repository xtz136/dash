from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    pass
