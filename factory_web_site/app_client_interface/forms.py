import re
from django import forms
from django.forms import ValidationError
from .models import Order

class OrderForm(forms.ModelForm):
    CHOICES = (
    ("Ремонт", "Ремонт"),
    ("Создание детали по чертежам", "Создание детали по чертежам"),
    ("Создание детали с нуля", "Создание детали с нуля")
    )
    email = forms.CharField(label="Адрес электронной почты:")
    description = forms.CharField(label="Комментарий:", widget=forms.Textarea, required=False)
    order_type = forms.ChoiceField(label="Выберите тип услуги:", choices=CHOICES)
    files = forms.FileField(label="Загрузите архив с файлами проекта (при наличии)", required=False)

    class Meta():
        model = Order
        fields = ['email', 'description', "order_type", "files"]

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        self.filename = kwargs.pop('filename', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'order-email-field input-field'})
        self.fields['description'].widget.attrs.update({'class': 'textarea-order-field input-field'})
        self.fields['order_type'].widget.attrs.update({'class': 'order-type-field input-field'})
        self.fields['files'].widget.attrs.update({'class': 'fileinput-order-field input-field'})
        if current_user is not None and current_user.is_authenticated and current_user.client_info is not None:
            self.fields['email'].initial = current_user.client_info.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError('Введён некорректный почтовый адрес.')
        return email

    def clean_files(self):
        files = self.cleaned_data.get('files')
        valid_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
        if self.filename is not None and not any(self.filename.endswith(ext) for ext in valid_extensions):
            raise ValidationError('Файл должен быть архивом.')
        if self.filename is None and files is None and self.cleaned_data.get('order_type') == "Создание детали по чертежам":
            raise ValidationError('Должны быть загружены файлы проекта.')
        if files is not None and not any(files.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError('Файл должен быть архивом.')
        return files

        
