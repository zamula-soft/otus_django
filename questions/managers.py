from django.db import models
from django.db.models import Count


class QuestionRelationsQuerySet(models.QuerySet):

    def num_answers(self):
        return self.annotate(num_answers=Count('answers', distinct=True))

    def tags(self):
        return self.prefetch_related('tags')

    def users(self):
        return self.prefetch_related('user')


class QuestionRelationsManager(models.Manager):
    def get_queryset(self):
        return QuestionRelationsQuerySet(self.model, using=self._db)

    def num_answers(self):
        return self.get_queryset().num_answers()

    def tags(self):
        return self.self.get_queryset().tags()

    def users(self):
        return self.self.get_queryset().users()

    def trending(self, limit):
        return self.get_queryset().filter(rank__gt=0).order_by('-rank', '-date_pub')[0:limit]