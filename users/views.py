import random
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.models import User

from config import settings

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, UserListForm
from users.models import User


class UserLoginView(LoginView):
    model = User
    success_url = reverse_lazy('newsletter:newslettermessage_list')
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    model = User
    success_url = reverse_lazy('blog:blog_list')


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_success_message(self, cleaned_data):
        return ('Вам на почту отправлено письмо, '
                'для прохождения верификации перейдите по ссылку в письме')

    def form_valid(self, form):
        """Верификация по ссылке через почту"""
        new_user = form.save()
        code = ''.join(random.sample('0123456789', 6))
        new_user.verify_code = code
        new_user.is_active = False
        print('new_user.email')
        send_mail(
            'Верификация',
            f'Перейдите по ссылке для верификации: '
            f'http://127.0.0.1:8000/users/verification/{code}',
            EMAIL_HOST_USER,
            [new_user.email]
        )
        return super().form_valid(form)


def verification(request, code):
    user = User.objects.get(verify_code=code)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Отключаем необходимость получения pk, получая его из запроса"""
        return self.request.user


def generate_new_password(request):
    new_pass = User.objects.make_random_password()
    request.user.set_password(new_pass)
    request.user.save()
    send_mail(
        'Вы сменили пароль ',
        f'Ваш новый пароль: {new_pass}',
        EMAIL_HOST_USER,
        [request.user.email]
    )
    messages.success(request,
                     'Вам на почту отправлено письмо '
                     'с новым паролем для вашего аккаунта')
    return redirect(reversed('mainapp:blog_list'))


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    form_class = UserListForm

    def test_func(self):
        return self.request.user.is_staff


@permission_required('users.set_is_active')
def status_user(request, pk):
    """Контроллер смены статуса пользователя"""
    user = User.objects.get(pk=pk)
    if not user.is_superuser:
        if user.is_active is True:
            user.is_active = False
            user.save()
        elif user.is_active is False:
            user.is_active = True
            user.save()
        return redirect(reverse('users:user_list'))


