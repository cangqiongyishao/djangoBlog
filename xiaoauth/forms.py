from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': 'Please type username',
        'max_length': 'length of username between 2-20',
        'min_length': 'length of username between 2-20'})
    email = forms.EmailField(error_messages={'required': 'Please enter email',
                                             'invalid': 'Please enter correct email'})

    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('Email exists')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('Not correct email or captcha')
        captcha_model.delete()
        return captcha


class LoginFrom(forms.Form):
    email = forms.EmailField(error_messages={'required': 'Please enter email',
                                             'invalid': 'Please enter correct email'})
    password = forms.CharField(max_length=20, min_length=6)
    remember = forms.IntegerField(required=False)
