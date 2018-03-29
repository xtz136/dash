from django.conf.urls import url
from django.views.generic import RedirectView
from .views import index, company, people, entity_list, entity

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name="index")),
    url(r'^index$', index.Index.as_view(), name='index'),
    url(r'^api/people$', people.PeopleApiView.as_view(), name='api.people'),
    url(r'^api/company$',
        company.CompanyApiView.as_view(), name='api.company'),
    url(r'^api/entity$',
        entity.EntityApiView.as_view(), name='api.entity'),
    url(r'^api/entity_list$',
        entity_list.EntityListApiView.as_view(), name='api.entity_list'),
]
