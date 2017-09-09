from django.forms import ModelForm
from crm.models import Company


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
