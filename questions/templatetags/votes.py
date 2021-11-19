from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_user_voted_for(context, model_name, model_pk, vote):
    votes = context.get('votes')
    # return votes.get(model_name).get(model_pk)
    
    return vote
