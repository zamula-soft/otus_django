from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        if v:
            query[k] = v
        elif k in query:
            del query[k]
    return query.urlencode()


