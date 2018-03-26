from django.conf.urls import url
from django.views.generic import RedirectView
from .views import index, entity, company

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="index")),
    url(r'^index$', index.index, name='index'),
    url(r'^entity$', entity.Entity.as_view(), name='entity'),
    url(r'^api/company$', company.CompanyApiView, name='api.company'),
]
