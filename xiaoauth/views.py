from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginFrom
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def xiaologin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginFrom(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('email or password incorrect')
                # form.add_error('email', 'email or password incorrect')
                # return render(request, 'login.html', context={form: form})
                return redirect(reverse('xiaoauth:login'))


def xiaologout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('xiaoauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('xiaoauth:register'))
            # return render(request, 'register.html', context={'form': form})


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': 'Must be email'})
    captcha = ''.join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail('XiaoBlog captcha', message=f'your captcha is:{captcha}', recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'message': 'Email send successfully'})
