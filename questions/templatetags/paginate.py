from django import template
from django.core.paginator import Paginator

register = template.Library()


@register.simple_tag(takes_context=True)
def paginate(context, **kwargs):
    return Paginator(context, 10)
