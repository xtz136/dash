from django.conf.urls import url
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from .views import index, company

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="index")),
    url(r'^index$', index.Index.as_view(), name='index'),
    url(r'^api/company$', company.CompanyApiView.as_view(), name='api.company'),
]
