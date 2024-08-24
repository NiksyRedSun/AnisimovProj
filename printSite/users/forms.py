from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
import re


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    error_messages = {
        'invalid_login': "Неверный E-mail или пароль. Пожалуйста, попробуйте снова."
    }

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    phone_num = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone_num', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        model = get_user_model()
        if model.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        model = get_user_model()
        if model.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже зарегистрирован!")
        return username

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        if not re.match(r'^(\+7|8)\d{10}$', phone_num):
            raise forms.ValidationError(
                "Введите номер телефона в формате +75556667799 или 85556667799"
            )
        return phone_num



class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone_num = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileUserForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        model = get_user_model()
        if model.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        model = get_user_model()
        if model.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Пользователь с таким именем уже зарегистрирован!")
        return username

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        if not re.match(r'^(\+7|8)\d{10}$', phone_num):
            raise forms.ValidationError(
                "Введите номер телефона в формате +75556667799 или 85556667799"
            )
        return phone_num

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone_num']
        labels = {
            'username': 'Логин',
            'email': 'E-mail',
            'phone_num': 'Номер телефона',
        }




class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


