import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView

from .forms import QuestionAddForm, AnswerAddForm
from .models import Question, Answer
from .utils import send_email_about_new_answer

logger = logging.getLogger(__name__)


class QuestionList(ListView):
    paginate_by = settings.QUESTIONS_PER_PAGE
    model = Question
    template_name = 'questions/index.html'
    queryset = Question.objects_related.num_answers().tags().users()

    def get_ordering(self):
        order_by = self.request.GET.get('order_by', None)
        if order_by == 'rank':
            ordering = ('-rank', '-date_pub',)
        else:
            ordering = ('-date_pub',)
        return ordering


class QuestionSearch(ListView):
    paginate_by = settings.QUESTIONS_PER_PAGE
    model = Question
    template_name = 'questions/search.html'
    queryset = Question.objects_related.num_answers().tags().users()
    ordering = ('-rank', '-date_pub',)

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.GET.get('t', None)
        if name:
            queryset = queryset.filter(tags__name=name)
        search_str = self.request.GET.get('s', None)
        if search_str:
            if 'tag:' in search_str:
                name = search_str[4:].strip()
                if name:
                    queryset = queryset.filter(tags__name=name)
            else:
                queryset = queryset.filter(Q(title__contains=search_str) | Q(content__contains=search_str))

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionAddForm
    template_name = 'questions/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreate, self).form_valid(form)


class QuestionDetail(View):
    template_name = 'questions/view.html'
    form_class = AnswerAddForm

    def get_question(self, pk):
        return get_object_or_404(Question.objects.select_related('user'), pk=pk)

    def paginate_answers(self, request, question):
        page = request.GET.get('page')
        answers_list = Answer.objects.filter(question=question). \
            prefetch_related('user'). \
            order_by('-rank', '-date_pub')

        paginator = Paginator(answers_list, settings.ANSWERS_PER_PAGE)
        return paginator.get_page(page)

    def get(self, request, pk):
        question = self.get_question(pk)

        ctx = dict()
        ctx['question'] = question
        ctx['page_obj'] = self.paginate_answers(request, question)
        ctx['form'] = self.form_class()

        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        question = self.get_question(pk)

        form = self.form_class(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            send_email_about_new_answer(self.request, answer, question)
            return redirect(reverse_lazy('questions:detail', kwargs={'pk': pk}))

        ctx = dict()
        ctx['question'] = question
        ctx['page_obj'] = self.paginate_answers(request, question)
        ctx['form'] = self.form_class()
        return render(request, self.template_name, ctx)


class QuestionAnswerAward(LoginRequiredMixin, View):

    def get(self, request, pk, answer_id):
        Answer.objects.filter(pk=answer_id, question_id=pk, question__user=request.user).\
            update(is_right=Q(is_right=False))
        return redirect(request.META.get('HTTP_REFERER'))