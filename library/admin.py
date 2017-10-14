from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from .models import Item, Receipt


@admin.register(Item)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("name", "company_title", "note", "qty", "status",
                    "receiver",
                    "borrower",  "received_at", "return_date")
    search_fields = ("item", "company_title", "note")
    list_filter = ("status", )
    raw_id_fields = ("company", )


@admin.register(Receipt)
class ReceiptModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'count', 'type', 'created',)
