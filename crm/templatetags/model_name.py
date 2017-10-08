from django import template

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
