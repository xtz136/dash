from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from crm.forms import PreferenceForm


@login_required
def profile_view(request):
    if request.method == "POST":
        form = PreferenceForm(data=request.POST)
        form.is_valid()
        profile = request.user.profile
        profile.preference.update(**dict(form.cleaned_data))
        profile.save()
        return HttpResponse('ok')
    return HttpResponseForbidden('fail')
