from django.forms import ModelForm
from django import forms
from django.utils.timezone import now

from taggit.forms import TagField
from ajax_select.fields import AutoCompleteField, AutoCompleteSelectField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Fieldset, Row
from crispy_forms.bootstrap import PrependedText


from core.models import Attachment
from crm.models import Company, ShareHolder


class UserAutoSelectForm(forms.Form):
    user = AutoCompleteField(
        'user', label='用户', required=True)


class BorrowerAutoSelectForm(forms.Form):
    user = AutoCompleteField(
        'user', label='借用者', required=True)


class AutoCompanyForm(forms.Form):
    """公司搜索表单"""
    q = AutoCompleteField('company', show_help_text=False)


class PreferenceForm(forms.Form):
    company_list_fields = forms.MultipleChoiceField(
        required=False,
        choices=[(f.name, f.verbose_name.title())
                 for f in Company._meta.fields if hasattr(f, 'verbose_name')]
    )


class CompanyModelForm(forms.ModelForm):
    local_tax_office = AutoCompleteSelectField(
        'local_tax', label='地税局', show_help_text=False, required=False)

    national_tax_office = AutoCompleteSelectField(
        'national_tax', label='国税局', show_help_text=False, required=False)

    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly', False)
        super(CompanyModelForm, self).__init__(*args, **kwargs)

        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.form_method = 'POST'
        helper.label_class = 'col-lg-2'
        helper.form_tag = False
        helper.field_class = 'col-lg-10'
        helper.layout = Layout(

            Fieldset('公司信息',
                     'title', 'alias',
                     'industry', 'type', 'scale_size',
                     'credit_rating', 'taxpayer_type',
                     'status', 'ic_status',
                     'tax_disk',
                     'ss_declared', 'has_customer_files',
                     'registered_capital',
                     'address', 'op_address',
                     'uscc', 'business_license',
                     'website', 'salesman', 'bookkeeper',
                     PrependedText('registered_at',
                                   '<i class="fa fa-calendar"></i>'),
                     PrependedText('expired_at',
                                   '<i class="fa fa-calendar"></i>'),
                     PrependedText('tax_declared_begin',
                                   '<i class="fa fa-calendar"></i>'),
                     'special_taxes',
                     PrependedText('contactor',
                                   '<i class="fa fa-user-circle"></i>'),
                     PrependedText('contactor_phone',
                                   '<i class="fa fa-phone"></i>'),
                     PrependedText('tags',
                                   '<i class="fa fa-tags"></i>',
                                   css_class="tagsinput"),
                     'note'),

            Fieldset('电子税局信息',
                     PrependedText('tax_username',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('tax_password',
                                   '<i class="fa fa-key"></i>')),

            Fieldset('银行信息',
                     'ss_number',
                     PrependedText('ss_date',
                                   '<i class="fa fa-calendar"></i>'),
                     'taxpayer_bank', 'taxpayer_account',
                     'ss_bank', 'ss_account',
                     'individual_bank', 'individual_account'
                     ),

            Fieldset('国税',
                     'national_tax_office',
                     'national_tax_id',
                     PrependedText('national_tax_staff',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('national_tax_phone',
                                   '<i class="fa fa-phone"></i>')),
            Fieldset('地税',
                     'local_tax_office',
                     'local_tax_id',
                     'local_tax_sn',
                     PrependedText('local_tax_staff',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('local_tax_phone',
                                   '<i class="fa fa-phone"></i>')),
            Fieldset('海关信息',
                     'custom_entry_no',
                     'custom_org_code',
                     'custom_register_no',
                     PrependedText('custom_registered_at',
                                   '<i class="fa fa-calendar"></i>'),
                     PrependedText('custom_expired_at',
                                   '<i class="fa fa-calendar"></i>'),
                     'premise'))
        self.helper = helper

        if readonly:
            for field in self.fields:
                self.fields[field].disabled = True


class CompanyFormSet(forms.ModelForm):
    local_tax_office = AutoCompleteSelectField(
        'local_tax', label='地税局', show_help_text=False, required=False)

    national_tax_office = AutoCompleteSelectField(
        'national_tax', label='国税局', show_help_text=False, required=False)

    class Meta:
        model = Company
        fields = '__all__'


class ShareHolderModelForm(forms.ModelForm):

    info = forms.CharField(required=False)

    class Meta:
        fields = ('name', 'role', 'sfz', 'phone',
                  'share', 'is_contactor', 'info')
        model = ShareHolder


class AttachmentModelForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'file_type', 'file')
        model = Attachment
