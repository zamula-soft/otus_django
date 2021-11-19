from django.contrib import admin

from .models import Question, Tag, Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_pub', 'rank')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'question', 'user', 'is_right', 'date_pub', 'rank')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag)
admin.site.register(Answer, AnswerAdmin)