from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic import CreateView


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "crm/registration.html"

    def get_success_url(self):
        return reverse('crm:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        return super(UserCreateView, self).form_valid(form)
