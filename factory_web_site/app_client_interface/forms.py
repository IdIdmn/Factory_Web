from pydoc import cli
import re
from django import forms
from django.forms import ValidationError
from django.db.models import Q
from .models import Order, Client

def is_Client(user):
    return user.groups.filter(name='Client').exists()


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
        fields = ['description', "order_type", "files"]

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        self.filename = kwargs.pop('filename', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'order-email-field input-field'})
        self.fields['description'].widget.attrs.update({'class': 'textarea-order-field input-field'})
        self.fields['order_type'].widget.attrs.update({'class': 'order-type-field input-field'})
        self.fields['files'].widget.attrs.update({'class': 'fileinput-order-field input-field'})
        if current_user is not None and current_user.is_authenticated and is_Client(current_user) and current_user.client_info is not None:
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

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            client, created = Client.objects.get_or_create(email=self.cleaned_data.get("email"))
            order.client = client
            order.save()
        return order
        

class ClientEditForm(forms.ModelForm):
    email = forms.CharField(label="Адрес электронной почты")
    full_name = forms.CharField(label="ФИО")
    phone_number = forms.CharField(label="Номер телефона")

    class Meta:
        model = Client
        fields = ["full_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'short-text-field input-field'})
        self.fields['full_name'].widget.attrs.update({'class': 'short-text-field input-field'})
        self.fields['phone_number'].widget.attrs.update({'class': 'short-text-field input-field'})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError("Некорректный почтовый адрес")
        if Client.objects.filter(Q(email=email) & Q(full_name__isnull=False)).count() and email != self.email:
            raise ValidationError("Почта уже занята")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r"[A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+$", full_name):
            raise ValidationError("Введите ФИО корректно")
        return full_name
    
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
        return "7" + re.sub(r"[\s\+\(\)\-]", "",phone_number)[1:]

    def save(self, commit=True):
        client = Client.objects.get(email=self.email)
        if commit:
            try:
                new_client = Client.objects.get(email = self.cleaned_data.get("email"))
                new_client.user = client.user
                client.user = None
                client.full_name = None
                client.phone_number = None           
                client.save()
                new_client.full_name = self.cleaned_data.get("full_name")
                new_client.phone_number = self.cleaned_data.get("phone_number")
                new_client.save()
            except Client.DoesNotExist:
                client.email = self.cleaned_data.get("email")
                client.full_name = self.cleaned_data.get("full_name")
                client.phone_number = self.cleaned_data.get("phone_number")
                client.save()
        return client


class OrderSearchForm(forms.Form):
    CHOICES = (
    ("order_type", "типу услуги"),
    ("cost", "цене"),
    ("date", "дате"),
    ("date_interval", "временному промежутку")
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field', "placeholder" : "ремонт"})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_type":
                if not re.match(r"[ а-яА-ЯёЁ]+$", value):
                    raise ValidationError("Некорректно введён тип услуг.")
            elif search_column == "date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value):
                    raise ValidationError("Дата введена некорректно.")
        return value
    
    def clean_interval_start(self):
        search_column = self.cleaned_data.get("search_column")
        start_value = self.cleaned_data.get("interval_start")
        if search_column == "cost":
            if start_value is not None and start_value:
                if not re.match(r"\d+$" , start_value):
                    raise ValidationError("Начальная сумма введена некорректно.")
            else:
                start_value = "0"
        elif search_column == "date_interval":
            if start_value is not None and start_value:
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "00.00.0001"
        return start_value
    
    def clean_interval_end(self):
        search_column = self.cleaned_data.get("search_column")
        end_value = self.cleaned_data.get("interval_end")
        if search_column == "cost":
            if end_value is not None and end_value:
                if not re.match(r"\d+$" , end_value):
                    raise ValidationError("Конечная сумма введена некорректно.")
            else:
                end_value = "2147483646"
        elif search_column == "date_interval":
            if end_value is not None and end_value:
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        return end_value
