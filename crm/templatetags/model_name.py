from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def model_name(value):
    if hasattr(value, 'model'):
        value = value.model
    return value._meta.verbose_name.title()


@register.simple_tag
def field_name(value, field):
    if hasattr(value, 'model'):
        value = value.model
    return value._meta.get_field(field).verbose_name.title()


@register.simple_tag
def controller_active(request, name):
    paths = [i.strip() for i in request.path.split('/') if i.strip()]
    return mark_safe(' class="active"' if paths[0] == name else "")


@register.simple_tag
def action_active(request, name):
    paths = [i.strip() for i in request.path.split('/') if i.strip()]
    if len(paths) >= 2:
        return mark_safe(' class="active"' if paths[1] == name else "")
    return ''
