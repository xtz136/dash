from django.views.generic.list import ListView
from django.utils import timezone

from accounting.models import Report
from ..utils import validate_month


class ReportListView(ListView):

    model = Report
    template_name = 'wechat/report_list.html'

    def get_queryset(self):
        queryset = super(ReportListView, self).get_queryset()
        lookups = {'company': self.request.user.profile.company}
        month = validate_month(self.request.GET.get('month', ''))
        if month:
            lookups['date__month'] = month.month
            lookups['date__year'] = month.year
        return queryset.filter(**lookups)

    def get_context_data(self):
        data = super(ReportListView, self).get_context_data()
        data['company'] = self.request.user.profile.company
        data['month'] = self.request.GET.get(
            'month', timezone.now().strftime('%Y-%m'))
        return data
