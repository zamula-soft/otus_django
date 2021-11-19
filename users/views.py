from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, FormView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView

from .forms import UserRegisterForm
from .models import UserProfile


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class UserLogoutView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    model = UserProfile
    fields = ('email', 'avatar')
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, pk=self.request.user.id)