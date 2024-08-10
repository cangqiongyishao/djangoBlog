import random
import string

from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.shortcuts import render

from .models import CaptchaModel


# Create your views here.

def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': 'Must be email'})
    captcha = ''.join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail('XiaoBlog captcha', message=f'your captcha is:{captcha}', recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'message': 'Email send successfully'})
