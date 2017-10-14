
from crispy_forms.helper import FormHelper


class MyTableInlineFormset(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MyTableInlineFormset, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'
