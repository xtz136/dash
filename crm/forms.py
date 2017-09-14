from django.forms import ModelForm
from crm.models import Company
from django import forms

from ajax_select.fields import AutoCompleteField


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ("title,type,registered_capital,industry,"
                  "taxpayer_type,scale_size,credit_rating,address,"
                  "op_address,uscc,business_license,website,salesman,"
                  "bookkeeper,registered_at,expired_at,status,ss_number,"
                  "ss_date,taxpayer_bank,taxpayer_account,ss_bank,ss_account,"
                  "individual_bank,individual_account,national_tax_office,"
                  "national_tax_id,national_tax_staff,national_tax_phone,"
                  "local_tax_office,local_tax_id,local_tax_sn,local_tax_staff,local_tax_phone").split(',')


class ItemAutoSelectForm(forms.Form):
    company = AutoCompleteField('company',
                                label="公司",
                                attrs={"size": 50},
                                help_text='输入公司名查找',
                                show_help_text=False,
                                required=True)
    receiver = AutoCompleteField(
        'user', label='签收人', required=True, show_help_text=False)


class UserAutoSelectForm(forms.Form):
    user = AutoCompleteField(
        'user', label='用户', required=True)


class BorrowerAutoSelectForm(forms.Form):
    user = AutoCompleteField(
        'user', label='借用者', required=True)
