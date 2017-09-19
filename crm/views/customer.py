from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomerView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/customer.html'
