from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LibraryView(LoginRequiredMixin, TemplateView):
    template_name = 'crm/library.html'
