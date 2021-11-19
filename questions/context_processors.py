from django.conf import settings

from votes.models import Vote
from .models import Question


def trending(request):
    questions = Question.objects_related.trending(settings.QUESTIONS_PER_PAGE)
    ctx = {'trending': questions}
    return ctx


def user_votes(request):
    ctx = {
        'question': {},
        'answer': {}
    }
    if request.user.is_authenticated:
        votes = Vote.objects.filter(user=request.user).select_related('content_type'). \
            values_list('content_type__model', 'object_id', 'vote').all()
        for (model_name, pk, vote) in votes:
            ctx[model_name][pk] = vote
    ctx = {'votes': ctx}
    return ctx