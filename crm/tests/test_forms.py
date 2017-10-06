import pytest
from .. import forms
pytestmark = pytest.mark.django_db


class TestCompany:
    def test_form(self):

        form = forms.CompanyModelForm(data={})
        assert form.is_valid() is False, '表单为空是不合法的'
        # assert 'body' in forms.errors

    def test_model_form(self):
        data = {'title': '我是公司抬头',
                'type': '有限责任公司',
                'industry': '汽配',
                'taxpayer_type': '小规模纳税人',
                'scale_size': '小型企业',
                'status': '有效',
                'credit_rating': '良好',
                'ic_status': '正常',
                'registered_capital': 1}
        model_form = forms.CompanyModelForm(data=data)
        assert model_form.is_valid()
        obj = model_form.save()
        assert obj.title == data['title']
