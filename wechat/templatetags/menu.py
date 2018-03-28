import datetime
from django.urls import reverse
from django import template
from django.template.loader import render_to_string


register = template.Library()

MENUS = [
    {'icon': 'area-chart', 'label': '查报表',
        'link': reverse('wechat:report-list')},
    {'icon': 'user-circle', 'label': '我的', 'link': reverse('wechat:user')},
]


@register.inclusion_tag('wechat/partials/menu.html', takes_context=True)
def render_menu(context):
    request = context['request']
    menus = [dict(d, active=(True if d['link'] == request.path else False))
             for d in MENUS]
    return {'request': request, 'menus': menus}
