from django.urls import path

from . import views

app_name = 'xiaoauth'

urlpatterns = [
    path('login', views.xiaologin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha')
]
