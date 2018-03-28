from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render


class Index(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'index.html')
