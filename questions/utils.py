import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


def send_email_about_new_answer(request, answer, question):
    ctx = {
        'author_username': question.user.username,
        'user_username': answer.user.username,
        'question': question,
        'question_link': request.build_absolute_uri(
            reverse_lazy('questions:detail', kwargs={'pk': question.pk}))
    }

    html_body = render_to_string('questions/emails/new_answer.html', ctx)
    txt_body = render_to_string('questions/emails/new_answer.txt', ctx)
    kwargs = {
        'subject': 'New answer to your question received',
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [question.user.email],
        'message': txt_body,
        'html_message': html_body
    }
    try:
        send_mail(**kwargs)
        logger.info('Email to %s successfully sent' % question.user.email)
    except Exception:
        logger.exception('Email to %s was failed' % question.user.email)