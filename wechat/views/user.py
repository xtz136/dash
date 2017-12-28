from django.views.generic.base import TemplateView


class UserView(TemplateView):

    template_name = "wechat/user.html"
