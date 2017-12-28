from django.views.generic.base import TemplateView


class UserView(TemplateView):

    template_name = "wechat/user.html"

    def get_context_data(self):
        data = super(UserView, self).get_context_data()
        data['navs'] = [
            {'label': '我的收藏', 'link': '#', 'icon': 'star-o'},
            {'label': '我的合同', 'link': '#', 'icon': 'file-text-o'},
            {'label': '设置', 'link': '#', 'icon': 'cog'},
        ]
        return data
