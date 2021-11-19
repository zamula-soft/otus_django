from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'avatar',)