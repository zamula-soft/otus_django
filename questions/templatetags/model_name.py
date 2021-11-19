from django import template

register = template.Library()


@register.simple_tag
def model_name(value):
    if hasattr(value, 'model'):
        value = value.model

    try:
        return value._meta.model_name
    except AttributeError:
        pass