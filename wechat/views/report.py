from django.views.generic.list import ListView
from django.utils import timezone

from accounting.models import Report


class ReportListView(ListView):

    model = Report
