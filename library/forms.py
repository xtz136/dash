from django import forms
from django.utils.timezone import now

from ajax_select.fields import AutoCompleteField, AutoCompleteSelectField
from crispy_forms.helper import FormHelper


class ItemAutoSelectForm(forms.Form):
    company = AutoCompleteField('company',
                                label="公司",
                                attrs={"size": 50},
                                help_text='输入公司名查找',
                                show_help_text=False,
                                required=True)
    receiver = AutoCompleteField(
        'user', label='签收人', required=True, show_help_text=False)
    received_at = forms.DateField(initial=now, label='签收时间')

    helper = FormHelper()
    helper.form_tag = False
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-10'


class SearchForm(forms.Form):
    """搜索表单"""
    q = forms.CharField(required=False,
                        widget=forms.TextInput(
                            attrs={'placeholder': '输入关键字搜索'}))


class BorrowerAutoSelectForm(forms.Form):
    borrower = AutoCompleteField('user',
                                 label='借用者',
                                 required=True,
                                 show_help_text=False)

    reason = forms.ChoiceField(label="事由", choices=(
        ('公事', '公事'),
    ))

    helper = FormHelper()
