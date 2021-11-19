from django.urls import path, re_path

from votes.views import VoteView
from .views import QuestionList, QuestionCreate, QuestionDetail, QuestionSearch, \
    QuestionAnswerAward

app_name = 'questions'

urlpatterns = [
    path('', QuestionList.as_view(), name='index'),
    path('add/', QuestionCreate.as_view(), name='add'),
    path("<int:pk>/", QuestionDetail.as_view(), name='detail'),
    path("search/", QuestionSearch.as_view(), name='search'),
    path("<int:pk>/answer/<int:answer_id>/award/", QuestionAnswerAward.as_view(), name='award'),
    re_path(r"^vote/(?P<object_name>question|answer)/(?P<object_id>\d+)/(?P<vote>up|down)/?$", VoteView.as_view(),
            name='vote')
]
