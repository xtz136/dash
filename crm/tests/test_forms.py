from .. import forms


class TestCompany:
    def test_form(self):
        form = forms.CompanyForm(data={})
        assert form.is_valid() is False, '表单为空是不合法的'

        form = forms.CompanyForm(data={})
        assert form.is_valid() is False, '表单为空是不合法的'
        # assert 'body' in forms.errors
