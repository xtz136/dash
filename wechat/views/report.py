from django.views.generic.list import ListView
from django.utils import timezone

from accounting.models import Report


class ReportListView(ListView):

    model = Report
    template_name = 'wechat/report_list.html'

    def get_queryset(self):
        queryset = super(ReportListView, self).get_queryset()
        queryset = queryset.filter(company=self.request.user.profile.company)
        print(queryset)
        return queryset

    def get_context_data(self):
        data = super(ReportListView, self).get_context_data()
        data['company'] = self.request.user.profile.company
        return data
