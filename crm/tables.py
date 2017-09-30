import django_tables2 as tables

from .models import Company


class CompanyTable(tables.Table):
    class Meta:
        fields = ('title', )
        attrs = {
            'class': 'table table-striped table-bordered table-hover my-table'
        }

        model = Company
