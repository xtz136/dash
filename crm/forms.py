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
        Fieldset.template = 'crm/fieldset.html'
        helper.layout = Layout(

            Fieldset('公司信息',
                     'title',
                     'industry', 'type', 'scale_size',
                     'taxpayer_type', 'rating',
                     'status', 'ic_status',
                     'has_customer_files',
                     'registered_capital',
                     'address', 'op_address',
                     'uscc', 'business_license',
                     'website', 'salesman', 'bookkeeper',
                     'legal_people', 'legal_phone',
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

            Fieldset('申报区',
                     'alias',
                     PrependedText('tax_username',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('tax_password',
                                   '<i class="fa fa-key"></i>'),

                     'batch',
                     'ss_declared',
                     'tax_disk',
                     'added_value_tax',
                     'income_tax',
                     'cut_tax',
                     'invoice',
                     'const_tax',
                     'special_taxes',
                     'declare_info'),

            Fieldset('银行信息',

                     'has_czk',
                     'ss_number',
                     'taxpayer_bank', 'taxpayer_account',
                     'ss_bank', 'ss_account',
                     'individual_bank', 'individual_account',

                     PrependedText('ss_date',
                                   '<i class="fa fa-calendar"></i>'),
                     ),

            Fieldset('国税信息',
                     'national_tax_office',
                     'national_tax_id',
                     PrependedText('national_tax_staff',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('national_tax_phone',
                                   '<i class="fa fa-phone"></i>')),
            Fieldset('地税信息',
                     'local_tax_office',
                     'local_tax_id',
                     'local_tax_sn',
                     PrependedText('local_tax_staff',
                                   '<i class="fa fa-user"></i>'),
                     PrependedText('local_tax_phone',
                                   '<i class="fa fa-phone"></i>')),
            Fieldset('海关信息',
                     'has_custom_info',
                     'custom_register_no',
                     'credit_rating',

                     PrependedText('custom_registered_at',
                                   '<i class="fa fa-calendar"></i>'),
                     PrependedText('custom_expired_at',
                                   '<i class="fa fa-calendar"></i>'),
                     ))
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


class BatchClientUpdateForm(forms.Form):
    """批量更新客户信息表单"""
    file = forms.FileField()
