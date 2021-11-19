from django import forms
from django.core.exceptions import ValidationError

from .models import Question, Tag, Answer


class CommaSeparatedTextField(forms.Field):
    widget = forms.TextInput()

    def to_python(self, value):
        tags = []
        if value:
            values = [i.lower() for i in map(str.strip, value.split(',')) if i]
            if len(values) <= 3:
                for tag_name in values:
                    tags.append(Tag.objects.get_or_create(name=tag_name)[0])
                return tags
            else:
                raise ValidationError('Max 3 tags is allowed')
        return tags


class QuestionAddForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea, label='Your Question')
    tags = CommaSeparatedTextField(required=False, help_text='You can specify up to 3 tags using a comma')

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags')


class AnswerAddForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='Your Answer')

    class Meta:
        model = Answer
        fields = ('content',)