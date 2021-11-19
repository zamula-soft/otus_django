from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import View

from .models import Vote


class VoteView(LoginRequiredMixin, View):
    redirect_field_name = None

    def get(self, request, object_name, object_id, vote):
        votes_map = {
            'up': Vote.VOTE_UP,
            'down': Vote.VOTE_DOWN
        }
        vote = votes_map.get(vote)
        if not vote:
            return HttpResponseBadRequest('Invalid vote value')
        app_label = request.resolver_match.app_name
        try:
            model_cls = apps.get_model(app_label, object_name)
            try:
                model_object = model_cls.objects.get(pk=object_id)
                model_object.vote(request.user, vote)
            except model_cls.DoesNotExist:
                return HttpResponseBadRequest('Invalid object id')
        except LookupError:
            return HttpResponseBadRequest('Invalid object name')
        if request.path != request.META.get('HTTP_REFERER'):
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('/')