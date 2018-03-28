from django.conf.urls import url
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from .views import entity, company

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="index")),
    url(r'^index$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^entity$', entity.Entity.as_view(), name='entity'),
    url(r'^api/company$', company.CompanyApiView.as_view(), name='api.company'),
]
