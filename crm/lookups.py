from ajax_select import register, LookupChannel
from django.contrib.auth.models import User
from .models import Company, TaxBureau


@register('company')
class CompanyLookup(LookupChannel):
    model = Company

    def get_query(self, q, request):
        return self.model.objects.filter(title__icontains=q)[:10]

    def format_item_display(self, item):
        return u"<span class='company'>%s</span>" % item.title


@register("local_tax")
class LocalTaxLookup(LookupChannel):
    model = TaxBureau

    def get_query(self, q, request):
        return self.model.objects.filter(
            bureau="local", full_title__icontains=q)[:10]


@register("national_tax")
class LocalTaxLookup(LookupChannel):
    model = TaxBureau

    def get_query(self, q, request):
        return self.model.objects.filter(
            bureau="national", full_title__icontains=q)[:10]


@register("user")
class UserLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
        return self.model.objects.filter(username__icontains=q)[:10]

    def format_item_display(self, item):
        return u"<span class='user'>%s</span>" % item.username
