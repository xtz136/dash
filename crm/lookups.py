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


@register("special_taxes")
class SpecialTaxesLookup(LookupChannel):
    taxes = ["文化事业费", "印花税", "网络发票"]

    def get_query(self, q, queryset):
        sep = ',' if ',' in q else ' '
        # 全角逗号
        if '，' in q:
            sep = '，'
        terms = [i.strip() for i in q.split(sep) if i.strip()]
        results = set()
        if terms:
            for t in terms:
                [results.add(z) for z in filter(lambda x: t in x, self.taxes)]
        return [",".join(sorted(list(results)))]

    def get_result(self, obj):
        print(obj)
        return obj
