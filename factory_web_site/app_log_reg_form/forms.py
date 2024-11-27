import re
from django import forms
from django.contrib.auth.models import User, Group
from django.forms import ValidationError
from django.db.models import Q
from app_client_interface.models import Client


class SignInForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field'})
        self.fields['password'].widget.attrs.update({'class': 'input-field'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not(User.objects.filter(username=username).count()):
            raise ValidationError("Нет такого пользователя")
        return username
    

class SignUpForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя", required=True)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, required=True)
    full_name = forms.CharField(label="ФИО")
    email = forms.CharField(label="Адрес электронной почты")
    phone_number = forms.CharField(label="Номер телефона")

    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field'})
        self.fields['password'].widget.attrs.update({'class': 'input-field'})
        self.fields['full_name'].widget.attrs.update({'class': 'input-field'})
        self.fields['email'].widget.attrs.update({'class': 'input-field'})
        self.fields['phone_number'].widget.attrs.update({'class': 'input-field'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count():
            raise ValidationError("Имя уже занято")
        return username
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r"[A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+$", full_name):
            raise ValidationError("Введите ФИО корректно")
        return full_name
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError("Некорректный почтовый адрес")
        if Client.objects.filter(Q(email=email) & Q(full_name__isnull=False)).count():
            raise ValidationError("Почта уже занята")
        return email
    
    def clean_phone_number(self):
        phone_template = r"[78]? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
        phone_template1 = r"[78]?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
        phone_template2 = r"\+?7? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
        phone_template3 = r"\+?7?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
        phone_number = self.cleaned_data.get("phone_number")
        is_phone_number_valid = bool(re.match(phone_template, phone_number)) or bool(re.match(phone_template1, phone_number)) or\
              bool(re.match(phone_template2, phone_number)) or bool(re.match(phone_template3, phone_number))
        if not is_phone_number_valid:
            raise ValidationError("Некорректный номер телефона")
        return phone_number


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='Client'))
            try:
                client = Client.objects.get(email=self.cleaned_data.get("email"))
                client.full_name = self.cleaned_data.get("full_name")
                client.phone_number = self.cleaned_data.get("phone_number")
                client.user = user
                client.save()
            except Client.DoesNotExist:
                Client.objects.create( user=user, full_name=self.cleaned_data["full_name"], email=self.cleaned_data["email"], phone_number=self.cleaned_data["phone_number"] )
        return user
        