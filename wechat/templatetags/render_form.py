import datetime
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.inclusion_tag('wechat/partials/form/input.html')
def render_input(field, t="text"):
    return {'field': field, 'type': t}


@register.inclusion_tag('wechat/partials/form/textarea.html')
def render_text(field):
    return {'field': field}
