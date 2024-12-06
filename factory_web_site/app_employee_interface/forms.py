import re
from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import *
from app_client_interface.models import *

def check_date(date):
    day = int(date[:2])
    month = int(date[3:5])
    year = int(date[6:])
    days_in_month = { 1: 31, 2: 29 if year % 4 == 0 else 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31 }
    if year > 0 and 0 < month <= 12 and 0 < day <= days_in_month[month]:
        return True
    return False


# ----------------------- Заказы -----------------------

class OrderSearchForm(forms.Form):
    CHOICES = (
    ("email", "по почтовому адресу"),
    ("order_type", "по типу заказа"),
    ("cost", "по цене"),
    ("date", "по дате"),
    ("date_interval", "по временному промежутку"),
    ("unprocessed_applications", "нерассмотренных заказов"),
    ("processed_applications", "рассмотренных заказов"),
    ("in_work", "заказов в работе"),
    ("executed", "выполненных заказов"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_type":
                if not re.match(r"[ а-яА-ЯёЁa-zA-Z]+$", value):
                    raise ValidationError("Некорректно введён тип услуг.")
            elif search_column == "date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value) or not check_date(start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.01.0001"
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value) or not check_date(end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        return end_value


class ChiefOrderSearchForm(forms.Form):
    CHOICES = (
    ("email", "по почтовому адресу"),
    ("order_type", "по типу заказа"),
    ("cost", "по цене"),
    ("date", "по дате"),
    ("date_interval", "по временному промежутку"),
    ("in_work", "заказов в работе"),
    ("executed", "выполненных заказов"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_type":
                if not re.match(r"[ а-яА-ЯёЁa-zA-Z]+$", value):
                    raise ValidationError("Некорректно введён тип услуг.")
            elif search_column == "date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value) or not check_date(start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.01.0001"
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value) or not check_date(end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        return end_value


class ChooseOrderSearchForm(forms.Form):
    CHOICES = (
    ("email", "по почтовому адресу"),
    ("order_type", "по типу заказа"),
    ("cost", "по цене"),
    ("date", "по дате"),
    ("date_interval", "по временному промежутку"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_type":
                if not re.match(r"[ а-яА-ЯёЁa-zA-Z]+$", value):
                    raise ValidationError("Некорректно введён тип услуг.")
            elif search_column == "date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value) or not check_date(start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.01.0001"
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value) or not check_date(end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        return end_value


class OrderCreateForm(forms.ModelForm):
    CHOICES = (
    ("Ремонт", "Ремонт"),
    ("Создание по чертежам", "Создание по чертежам"),
    ("Создание с нуля", "Создание с нуля")
    )
    email = forms.CharField(label="Адрес электронной почты")
    description = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)
    order_type = forms.ChoiceField(label="Тип заказа",choices=CHOICES)
    cost = forms.FloatField(label="Цена", required=False)
    files = forms.FileField(label="Архив с проектом",required=False)
    
    class Meta:
        model = Order
        fields = ["email", "description", "order_type", "cost", "files"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['description'].widget.attrs.update({'class': 'textarea-field input-field'})
        self.fields['order_type'].widget.attrs.update({'class': 'select-field input-field'})
        self.fields['cost'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['files'].widget.attrs.update({'class': 'fileinput-order-field'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError('Введён некорректный почтовый адрес.')
        return email

    def clean_files(self):
        files = self.cleaned_data.get('files')
        valid_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
        if files is None and self.cleaned_data.get('order_type') == "Создание детали по чертежам":
            raise ValidationError('Должны быть загружены файлы проекта.')
        if files is not None and not any(files.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError('Файл должен быть архивом.')
        return files
    
    def clean_cost(self):
        cost = self.cleaned_data.get("cost")
        if cost is not None and cost < 0:
            raise ValidationError('Введена некорректная сумма денег.')
        return cost
        
    def save(self, commit=True):
        order = super().save(commit=False)
        if self.cleaned_data.get("cost") is not None:
            order.status = "В работе"
        if commit:
            client, created = Client.objects.get_or_create(email=self.cleaned_data.get("email"))
            order.client = client
            order.save()
        return order


class OrderEditForm(forms.ModelForm):
    CHOICES = (
    ("Ремонт", "Ремонт"),
    ("Создание по чертежам", "Создание по чертежам"),
    ("Создание с нуля", "Создание с нуля")
    )
    email = forms.CharField(label="Адрес электронной почты")
    description = forms.CharField(label="Комментарий", widget=forms.Textarea, required=False)
    order_type = forms.ChoiceField(label="Тип заказа",choices=CHOICES)
    cost = forms.FloatField(label="Цена", required=False)
    
    class Meta:
        model = Order
        fields = ["email", "description", "order_type", "cost"]

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['description'].widget.attrs.update({'class': 'textarea-field input-field'})
        self.fields['order_type'].widget.attrs.update({'class': 'select-field input-field'})
        self.fields['cost'].widget.attrs.update({'class': 'common-field input-field'})
        if self.id is not None:
            self.fields['email'].initial = Order.objects.get(id=self.id).client.email
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError('Введён некорректный почтовый адрес.')
        return email
    
    def clean_cost(self):
        cost = self.cleaned_data.get("cost")
        if cost is not None and cost < 0:
            raise ValidationError('Введена некорректная сумма денег.')
        return cost
        
    def save(self, commit=True):
        order = Order.objects.get(id=self.id)
        client, created = Client.objects.get_or_create(email=self.cleaned_data.get("email"))
        order.client = client
        order.description = self.cleaned_data.get("description")
        order.cost = self.cleaned_data.get("cost")
        order.order_type = self.cleaned_data.get("order_type")
        if self.cleaned_data.get("cost") is None:
            order.status = "На рассмотрении"
        else:
            order.status = "В работе"
        if commit:
            order.save()
        return order

# ----------------------- Клиенты -----------------------

class ClientSearchForm(forms.Form):
    CHOICES = (
    ("email", "по почтовому адресу"),
    ("full_name", "по ФИО"),
    ("phone_number", "по номеру телефона"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})


    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "phone_number":
                phone_template = r"[78]? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
                phone_template1 = r"[78]?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
                phone_template2 = r"\+?7? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
                phone_template3 = r"\+?7?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
                is_phone_number_valid = bool(re.match(phone_template, value)) or bool(re.match(phone_template1, value)) or\
                    bool(re.match(phone_template2, value)) or bool(re.match(phone_template3, value))
                if not is_phone_number_valid:
                    raise ValidationError("Некорректный номер телефона")
                value = "7" + re.sub(r"[\s\+\(\)\-]", "", value)[1:]
            elif search_column == "full_name":
                if not re.match(r"[ A-Za-zа-яА-ЯёЁ]*$", value):
                    raise ValidationError("Введите ФИО корректно")
        return value


class ClientEditForm(forms.ModelForm):
    email = forms.CharField(label="Адрес электронной почты")
    full_name = forms.CharField(label="ФИО")
    phone_number = forms.CharField(label="Номер телефона")

    field_order = ['email', 'full_name', 'phone_number']

    class Meta:
        model = Client
        fields = ["full_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        self.email = Client.objects.get(id = self.id).email
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['full_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['phone_number'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError("Некорректный почтовый адрес")
        if Client.objects.filter(Q(email=email) & Q(full_name__isnull=False)).exists() and email != self.email:
            raise ValidationError("Почта уже занята")
        return email

    def clean_full_name(self):
        cur_client = Client.objects.get(id = self.id)
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r"[A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+$", full_name):
            raise ValidationError("Введите ФИО корректно")
        if cur_client.full_name is None:
            raise ValidationError("Заполнение ФИО недоступно. Запись клиента сперва должна быть привязана к аккаунту.")
        return full_name
    
    def clean_phone_number(self):
        cur_client = Client.objects.get(id = self.id)
        phone_template = r"[78]? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
        phone_template1 = r"[78]?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
        phone_template2 = r"\+?7? ?\(?\d{3}\)? ?\d{3}-?\d{2}-?\d{2}$"
        phone_template3 = r"\+?7?-?\d{3}-?\d{3}-?\d{2}-?\d{2}$"
        phone_number = self.cleaned_data.get("phone_number")
        is_phone_number_valid = bool(re.match(phone_template, phone_number)) or bool(re.match(phone_template1, phone_number)) or\
              bool(re.match(phone_template2, phone_number)) or bool(re.match(phone_template3, phone_number))
        if not is_phone_number_valid:
            raise ValidationError("Некорректный номер телефона")
        if cur_client.phone_number is None:
            raise ValidationError("Заполнение ФИО недоступно. Запись клиента сперва должна быть привязана к аккаунту.")
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


# ----------------------- Поставщики -----------------------

class VendorSearchForm(forms.Form):
    CHOICES = (
    ("email", "по почтовому адресу"),
    ("company_name", "по названию компании"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})


class VendorCreateForm(forms.ModelForm):
    email = forms.CharField(label="Адрес электронной почты")
    company_name = forms.CharField(label="Название компании")

    class Meta:
        model = Vendor
        fields = ["company_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['company_name'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError('Введён некорректный почтовый адрес.')
        if Vendor.objects.filter(email=email).exists():
            raise ValidationError("Одна из компаний в каталоге имеет данный почтовый адрес")
        return email
    
    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if Vendor.objects.filter(company_name=company_name).exists():
            raise ValidationError("Компания с таким названием уже занесена в список.")
        return company_name


class VendorEditForm(forms.ModelForm):
    email = forms.CharField(label="Адрес электронной почты")
    company_name = forms.CharField(label="Название компании")

    class Meta:
        model = Vendor
        fields = ["company_name", "email"]

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['company_name'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not (re.match(r"[^@\s]+\@[^@\s]+\.[^@\s]{2,}$", email) and email.count('.') > 0):
            raise ValidationError('Введён некорректный почтовый адрес.')
        if Vendor.objects.filter(email=email).exists() and email != Vendor.objects.get(id=self.id).email:
            raise ValidationError("Компания с такой почтой уже занесена в список.")
        return email
    
    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if Vendor.objects.filter(company_name=company_name).exists() and company_name != Vendor.objects.get(id=self.id).company_name:
            raise ValidationError("Компания с таким названием уже занесена в список.")
        return company_name
        
    def save(self, commit=True):
        vendor = Vendor.objects.get(id=self.id)
        vendor.email = self.cleaned_data.get('email')
        vendor.company_name = self.cleaned_data.get("company_name")
        if commit:
            vendor.save()
        return vendor

# ----------------------- Материалы -----------------------

class MaterialSearchForm(forms.Form):
    CHOICES = (
    ("vendor", "по названию компании"),
    ("metal_type", "по типу металла"),
    ("metal_grade", "по марке металла"),
    ("cost", "по цене"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_interval_start(self):
        search_column = self.cleaned_data.get("search_column")
        start_value = self.cleaned_data.get("interval_start")
        if search_column == "cost":
            if start_value is not None and start_value:
                if not re.match(r"\d+$" , start_value):
                    raise ValidationError("Начальная сумма введена некорректно.")
            else:
                start_value = "0"
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
        return end_value
    

class MaterialCreateForm(forms.ModelForm):
    company_name = forms.CharField(label="Название компании")
    metal_type = forms.CharField(label="Название сплава")
    metal_grade = forms.CharField(label="Марка металла")
    cost = forms.FloatField(label="Цена за единицу товара")

    field_order = ['company_name', 'metal_type', 'metal_grade', 'cost']

    class Meta:
        model = Material
        fields = ["metal_type", "metal_grade", "cost"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['metal_type'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['metal_grade'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['cost'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if not Vendor.objects.filter(company_name = company_name).exists():
            raise ValidationError("Компания с таким названием ещё не занесена в каталог")
        return company_name

    def clean_metal_grade(self):
        metal_grade = self.cleaned_data.get("metal_grade")
        metal_type = self.cleaned_data.get("metal_type")
        company_name = self.cleaned_data.get("company_name")
        if Vendor.objects.filter(company_name = company_name).exists():
            vendor = Vendor.objects.get(company_name=company_name)
            if Material.objects.filter(Q(metal_type=metal_type) & Q(metal_grade=metal_grade) & Q(vendor=vendor)).exists():
                raise ValidationError("Информация о данном сплаве от этого производителя уже занесена в каталог")
        return metal_grade

    def clean_cost(self):
        cost = self.cleaned_data.get("cost")
        if cost is not None and cost < 0:
            raise ValidationError('Введена некорректная сумма денег.')
        return cost
    
    def save(self, commit=True):
        material = super().save(commit=False)
        material.vendor = Vendor.objects.get(company_name = self.cleaned_data.get("company_name"))
        if commit:
            material.save()
        return material


class MaterialEditForm(forms.ModelForm):
    company_name = forms.CharField(label="Название компании")
    metal_type = forms.CharField(label="Название сплава")
    metal_grade = forms.CharField(label="Марка металла")
    cost = forms.FloatField(label="Цена за единицу товара")

    field_order = ['company_name', 'metal_type', 'metal_grade', 'cost']

    class Meta:
        model = Material
        fields = ["metal_type", "metal_grade", "cost"]
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['company_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['metal_type'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['metal_grade'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['cost'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['company_name'].initial = Vendor.objects.get(id=self.id).company_name

    def clean_company_name(self):
        company_name = self.cleaned_data.get("company_name")
        if not Vendor.objects.filter(company_name = company_name).exists():
            raise ValidationError("Компания с таким названием ещё не занесена в каталог")
        return company_name

    def clean_metal_grade(self):
        metal_grade = self.cleaned_data.get("metal_grade")
        metal_type = self.cleaned_data.get("metal_type")
        company_name = self.cleaned_data.get("company_name")
        cur_material = Material.objects.get(id=self.id)
        if Vendor.objects.filter(company_name = company_name).exists():
            vendor = Vendor.objects.get(company_name=company_name)
            if Material.objects.filter(Q(metal_type=metal_type) & Q(metal_grade=metal_grade) & Q(vendor=vendor)).exists() and \
                not (metal_type == cur_material.metal_type and metal_grade == cur_material.metal_grade and company_name == cur_material.vendor.company_name):
                raise ValidationError("Информация о данном сплаве от этого производителя уже занесена в каталог")
        return metal_grade

    def clean_cost(self):
        cost = self.cleaned_data.get("cost")
        if cost is not None and cost < 0:
            raise ValidationError('Введена некорректная сумма денег.')
        return cost
    
    def save(self, commit=True):
        material = material = Material.objects.get(id=self.id)
        material.vendor = Vendor.objects.get(company_name = self.cleaned_data.get("company_name"))
        material.cost = self.cleaned_data.get("cost")
        material.metal_type = self.cleaned_data.get("metal_type")
        material.metal_grade = self.cleaned_data.get("metal_grade")
        if commit:
            material.save()
        return material        

# ----------------------- Сотрудники -----------------------

class EmployeeSearchForm(forms.Form):
    CHOICES = (
    ("full_name", "по ФИО"),
    ("specialty", "по специальности"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "full_name":
                if not re.match(r"[ A-Za-zа-яА-ЯёЁ]*$", value):
                    raise ValidationError("Введите ФИО корректно")
        return value


class EmployeeCreateForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО")
    specialty = forms.CharField(label="Специальность")
    salary = forms.IntegerField(label="Зарплата")

    class Meta:
        model = Employee
        fields = ["full_name", "specialty", "salary"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['specialty'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['salary'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r"[A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+$", full_name):
            raise ValidationError("Введите ФИО корректно")
        return full_name

    def clean_specialty(self):
        specialty = self.cleaned_data.get("specialty")
        if not re.match(r"[ а-яА-ЯёЁ]+", specialty):
            raise ValidationError("Некорректное название специальности")
        return specialty

    def clean_salary(self):
        salary = self.cleaned_data.get("salary")
        if salary < 0:
            raise ValidationError("Некорректно введена заработная плата сотрудника")
        return salary


class EmployeeEditForm(forms.ModelForm):
    full_name = forms.CharField(label="ФИО")
    specialty = forms.CharField(label="Специальность")
    salary = forms.IntegerField(label="Зарплата")

    class Meta:
        model = Employee
        fields = ["full_name", "specialty", "salary"]
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['specialty'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['salary'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r"[A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+ [A-Za-zа-яА-ЯёЁ]+$", full_name):
            raise ValidationError("Введите ФИО корректно")
        return full_name

    def clean_specialty(self):
        specialty = self.cleaned_data.get("specialty")
        if not re.match(r"[ а-яА-ЯёЁ]+", specialty):
            raise ValidationError("Некорректное название специальности")
        return specialty

    def clean_salary(self):
        salary = self.cleaned_data.get("salary")
        if salary < 0:
            raise ValidationError("Некорректно введена заработная плата сотрудника")
        return salary

    def save(self, commit=True):
        employee = Employee.objects.get(id=self.id)
        employee.full_name = self.cleaned_data.get('full_name')
        employee.specialty = self.cleaned_data.get("specialty")
        employee.salary = self.cleaned_data.get("salary")
        if commit:
            employee.save()
        return employee

# ----------------------- Станки -----------------------

class MachineSearchForm(forms.Form):
    CHOICES = (
    ("serial_number", "по серийному номеру"),
    ("machine_name", "по названию"),
    ("specialty", "по специальности"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})


class MachineCreateForm(forms.ModelForm):
    serial_number = forms.CharField(label="Серийный номер")
    machine_name = forms.CharField(label="Название станка")
    specialty = forms.CharField(label="Специальность")

    class Meta:
        model = Machine
        fields = ["serial_number", "machine_name", "specialty"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['serial_number'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['machine_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['specialty'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get("serial_number")
        print(serial_number)
        if Machine.objects.filter(serial_number = serial_number).exists():
            raise ValidationError("Данный станок уже внесён в каталог")
        return serial_number

    def clean_machine_name(self):
        machine_name = self.cleaned_data.get("machine_name")
        print(machine_name)
        if not re.match(r"[ а-яА-ЯёЁ]+", machine_name):
            raise ValidationError("Некорректное название станка")
        return machine_name
    
    def clean_specialty(self):
        specialty = self.cleaned_data.get("specialty")
        print(specialty)
        if not re.match(r"[ а-яА-ЯёЁ]+", specialty):
            raise ValidationError("Некорректное название специальности")
        return specialty
    

class MachineEditForm(forms.ModelForm):
    serial_number = forms.CharField(label="Серийный номер")
    machine_name = forms.CharField(label="Название станка")
    specialty = forms.CharField(label="Специальность")

    class Meta:
        model = Machine
        fields = ["serial_number", "machine_name", "specialty"]
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['serial_number'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['machine_name'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['specialty'].widget.attrs.update({'class': 'common-field input-field'})

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get("serial_number")
        if Machine.objects.filter(serial_number = serial_number).exists() and serial_number != Machine.objects.get(id=self.id).serial_number:
            raise ValidationError("Данный станок уже внесён в каталог")
        return serial_number

    def clean_machine_name(self):
        machine_name = self.cleaned_data.get("machine_name")
        if not re.match(r"[ а-яА-ЯёЁ]", machine_name):
            raise ValidationError("Некорректное название станка")
        return machine_name
    
    def clean_specialty(self):
        specialty = self.cleaned_data.get("specialty")
        if not re.match(r"[ а-яА-ЯёЁ]", specialty):
            raise ValidationError("Некорректное название станка")
        return specialty
    
    def save(self, commit=True):
        machine = Machine.objects.get(id=self.id)
        machine.serial_number = self.cleaned_data.get("serial_number")
        machine.machine_name = self.cleaned_data.get("machine_name")
        machine.specialty = self.cleaned_data.get("specialty")
        if commit:
            machine.save()
        return machine

# ----------------------- Поставки -----------------------

class SupplySearchForm(forms.Form):
    CHOICES = (
    ("order_id", "по ID заказа"),
    ("material_id", "по ID материала"),
    ("quantity", "по количеству"),
    ("cost", "по цене"),
    ("date", "по дате"),
    ("date_interval", "по временному промежутку"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})
    
    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_id":
                if not re.match(r"\d+$", value):
                    raise ValidationError("Некорректно введён ID заказа.")
            elif search_column == "material_id":
                if not re.match(r"\d+$", value):
                    raise ValidationError("Некорректно введён ID материала.")
            elif search_column == "date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value) or not check_date(start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.01.0001"
        elif search_column == "quantity":
            if start_value is not None and start_value:
                if not re.match(r"\d+$" , start_value):
                    raise ValidationError("Начальное кол-во введено некорректно.")
            else:
                start_value = "0"
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
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value) or not check_date(end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        elif search_column == "quantity":
            if end_value is not None and end_value:
                if not re.match(r"\d+$" , end_value):
                    raise ValidationError("Конечное кол-во введено некорректно.")
            else:
                end_value = "2147483646"
        return end_value
    

class SupplyCreateForm(forms.ModelForm):
    order_id = forms.IntegerField(label="ID заказа")
    material_id = forms.IntegerField(label="ID материала")
    quantity = forms.IntegerField(label="Количество")

    field_order = ["order_id", "material_id", "quantity"]

    class Meta:
        model = Supply
        fields = ["quantity"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['material_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['quantity'].widget.attrs.update({'class': 'common-field input-field'})
    
    def clean_order_id(self):
        order_id = self.cleaned_data.get("order_id")
        if order_id < 0:
            raise ValidationError("Некорректный ID заказа")
        if not Order.objects.filter(id = order_id).exists():
            raise ValidationError("Не существует заказа с указанным ID")
        return order_id

    def clean_material_id(self):
        material_id = self.cleaned_data.get("material_id")
        if material_id < 0:
            raise ValidationError("Некорректный ID материала")
        if not Material.objects.filter(id = material_id).exists():
            raise ValidationError("Не существует материала с указанным ID")
        return material_id
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity < 0:
            raise ValidationError("В качестве количества введено некорректное число")
        return quantity
    
    def save(self, commit=True):
        supply = super().save(commit=False)
        supply.order = Order.objects.get(id = self.cleaned_data.get("order_id"))
        supply.material = Material.objects.get(id = self.cleaned_data.get("material_id"))
        supply.cost = float(self.cleaned_data.get("quantity")) * supply.material.cost
        if commit:
            supply.save()
        return supply


class SupplyEditForm(forms.ModelForm):
    order_id = forms.IntegerField(label="ID заказа")
    material_id = forms.IntegerField(label="ID материала")
    quantity = forms.IntegerField(label="Количество")

    field_order = ["order_id", "material_id", "quantity"]

    class Meta:
        model = Supply
        fields = ["quantity"]
    
    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['order_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['material_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['quantity'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['order_id'].initial = Supply.objects.get(id=self.id).order.id
        self.fields['material_id'].initial = Supply.objects.get(id=self.id).material.id
    
    def clean_order_id(self):
        order_id = self.cleaned_data.get("order_id")
        if order_id < 0:
            raise ValidationError("Некорректный ID заказа")
        if not Order.objects.filter(id = order_id).exists():
            raise ValidationError("Не существует заказа с указанным ID")
        return order_id

    def clean_material_id(self):
        material_id = self.cleaned_data.get("material_id")
        if material_id < 0:
            raise ValidationError("Некорректный ID материала")
        if not Material.objects.filter(id = material_id).exists():
            raise ValidationError("Не существует материала с указанным ID")
        return material_id
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        if quantity < 0:
            raise ValidationError("В качестве количества введено некорректное число")
        return quantity
    
    def save(self, commit=True):
        supply = Supply.objects.get(id = self.id)
        supply.order = Order.objects.get(id = self.cleaned_data.get("order_id"))
        supply.material = Material.objects.get(id = self.cleaned_data.get("material_id"))
        supply.cost = self.cleaned_data.get("quantity") * supply.material.cost
        if commit:
            supply.save()
        return supply

# ----------------------- Сотрудники -----------------------

class ScheduleSearchForm(forms.Form):
    CHOICES = (
    ("order_id", "по ID заказа"),
    ("employee_id", "по ID сотрудника"),
    ("machine_id", "по ID станка"),
    ("start_date", "по дате начала"),
    ("end_date", "по дате окончания"),
    ("date_interval", "по временному промежутку"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})
    

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "order_id":
                if not re.match(r"\d+$", value):
                    raise ValidationError("Некорректно введён ID заказа.")
            elif search_column == "employee_id":
                if not re.match(r"\d+$", value):
                    raise ValidationError("Некорректно введён ID сотрудника.")
            elif search_column == "machine_id":
                if not re.match(r"\d+$", value):
                    raise ValidationError("Некорректно введён ID станка.")
            elif search_column == "start_date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
                    raise ValidationError("Дата начала введена некорректно.")
            elif search_column == "end_date":
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", value) or not check_date(value):
                    raise ValidationError("Дата окончания введена некорректно.")
        return value
    
    def clean_interval_start(self):
        search_column = self.cleaned_data.get("search_column")
        start_value = self.cleaned_data.get("interval_start")
        if search_column == "date_interval":
            if start_value is not None and start_value:
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_value) or not check_date(start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.01.0001"
        return start_value
    
    def clean_interval_end(self):
        search_column = self.cleaned_data.get("search_column")
        end_value = self.cleaned_data.get("interval_end")
        if search_column == "date_interval":
            if end_value is not None and end_value:
                if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_value) or not check_date(end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "30.12.9999"
        return end_value


class ScheduleCreateForm(forms.ModelForm):
    order_id = forms.IntegerField(label="ID заказа")
    employee_id = forms.IntegerField(label="ID сотрудника")
    machine_id = forms.IntegerField(label="ID станка")
    start_date = forms.CharField(label="Дата начала")
    end_date = forms.CharField(label="Дата окончания")

    field_order = ["order_id", "employee_id", "machine_id", "start_date", "end_date"]

    class Meta:
        model = Schedule
        fields = ["start_date", "end_date"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['employee_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['machine_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['start_date'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['end_date'].widget.attrs.update({'class': 'common-field input-field'})
    
    def clean_order_id(self):
        order_id = self.cleaned_data.get("order_id")
        if order_id < 0:
            raise ValidationError("Некорректный ID заказа")
        if not Order.objects.filter(id = order_id).exists():
            raise ValidationError("Не существует заказа с указанным ID")
        return order_id
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        if employee_id < 0:
            raise ValidationError("Некорректный ID сотрудника")
        if not Employee.objects.filter(id = employee_id).exists():
            raise ValidationError("Не существует сотрудника с указанным ID")
        return employee_id
    
    def clean_machine_id(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        if machine_id < 0:
            raise ValidationError("Некорректный ID станка")
        if not Machine.objects.filter(id = machine_id).exists():
            raise ValidationError("Не существует станка с указанным ID")
        if Employee.objects.filter(id = employee_id).exists():
            if Machine.objects.get(id = machine_id).specialty not in Employee.objects.get(id = employee_id).specialty:
                raise ValidationError("Сотрудник не обладает нужными навыками для работы за данным станком.") 
        return machine_id
    
    def clean_start_date(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        start_date = self.cleaned_data.get("start_date")
        if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_date) or not check_date(start_date):
            raise ValidationError("Дата начала работ введена некорректно.")
        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
        if Employee.objects.filter(id = employee_id).exists():
            if Schedule.objects.filter(Q(employee__id=employee_id) & Q(start_date__lte=start_date) & Q(end_date__gte=start_date)).exists():
                raise ValidationError("Данный сотрудник занят в указанный промежуток времени (некорректная дата начала)")
        if Machine.objects.filter(id = machine_id).exists():
            if Schedule.objects.filter(Q(machine__id=machine_id) & Q(start_date__lte=start_date) & Q(end_date__gte=start_date)).exists():
                raise ValidationError("Данный станок занят в указанный промежуток времени (некорректная дата начала)")
        return start_date
    
    def clean_end_date(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        end_date = self.cleaned_data.get("end_date")
        if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_date) or not check_date(end_date):
            raise ValidationError("Дата окончания работ введена некорректно.")
        end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")
        start_date = self.cleaned_data.get("start_date")
        if start_date is not None:
            if end_date < start_date:
                raise ValidationError("Дата окончания не может быть раньше даты начала")
            if Employee.objects.filter(id = employee_id).exists():
                if Schedule.objects.filter(Q(employee__id=employee_id) & Q(start_date__lte=end_date) & Q(end_date__gte=end_date)).exists():
                    raise ValidationError("Данный сотрудник занят в указанный промежуток времени (некорректная дата окончания)")
                elif Schedule.objects.filter(Q(employee__id=employee_id) & Q(start_date__gte=start_date) & Q(end_date__lte=end_date)).exists():
                    raise ValidationError("Данный сотрудник занят в указанный промежуток времени")
            if Machine.objects.filter(id = machine_id).exists():
                if Schedule.objects.filter(Q(machine__id=machine_id) & Q(start_date__lte=end_date) & Q(end_date__gte=end_date)).exists():
                    raise ValidationError("Данный станок занят в указанный промежуток времени (некорректная дата окончания)")
                elif Schedule.objects.filter(Q(machine__id=machine_id) & Q(start_date__gte=start_date) & Q(end_date__lte=end_date)).exists():
                    raise ValidationError("Данный станок занят в указанный промежуток времени")
        return end_date
    
    def save(self, commit=True):
        schedule_item =  super().save(commit=False)
        schedule_item.order = Order.objects.get(id=self.cleaned_data.get("order_id"))
        schedule_item.employee = Employee.objects.get(id=self.cleaned_data.get("employee_id"))
        schedule_item.machine = Machine.objects.get(id=self.cleaned_data.get("machine_id"))
        if commit:
            schedule_item.save()
        return schedule_item


class ScheduleEditForm(forms.ModelForm):
    order_id = forms.IntegerField(label="ID заказа")
    employee_id = forms.IntegerField(label="ID сотрудника")
    machine_id = forms.IntegerField(label="ID станка")
    start_date = forms.CharField(label="Дата начала")
    end_date = forms.CharField(label="Дата окончания")

    field_order = ["order_id", "employee_id", "machine_id", "start_date", "end_date"]

    class Meta:
        model = Schedule
        fields = ["start_date", "end_date"]
    
    def __init__(self, *args, **kwargs):
        if kwargs.get("initial") is not None:
            if type(kwargs["initial"]["start_date"]) != str and type(kwargs["initial"]["end_date"]) != str:
                kwargs["initial"]["start_date"] = datetime.date.strftime(kwargs["initial"]["start_date"], "%d.%m.%Y")
                kwargs["initial"]["end_date"] = datetime.date.strftime(kwargs["initial"]["end_date"], "%d.%m.%Y")
        self.id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)
        self.fields['order_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['employee_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['machine_id'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['start_date'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['end_date'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['order_id'].initial = Schedule.objects.get(id=self.id).order.id
        self.fields['employee_id'].initial = Schedule.objects.get(id=self.id).employee.id
        self.fields['machine_id'].initial = Schedule.objects.get(id=self.id).machine.id
    
    def clean_order_id(self):
        order_id = self.cleaned_data.get("order_id")
        if order_id < 0:
            raise ValidationError("Некорректный ID заказа")
        if not Order.objects.filter(id = order_id).exists():
            raise ValidationError("Не существует заказа с указанным ID")
        return order_id
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        if employee_id < 0:
            raise ValidationError("Некорректный ID сотрудника")
        if not Employee.objects.filter(id = employee_id).exists():
            raise ValidationError("Не существует сотрудника с указанным ID")
        return employee_id
    
    def clean_machine_id(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        if machine_id < 0:
            raise ValidationError("Некорректный ID станка")
        if not Machine.objects.filter(id = machine_id).exists():
            raise ValidationError("Не существует станка с указанным ID")
        if Employee.objects.filter(id = employee_id).exists():
            if Machine.objects.get(id = machine_id).specialty not in Employee.objects.get(id = employee_id).specialty:
                raise ValidationError("Сотрудник не обладает нужными навыками для работы за данным станком.") 
        return machine_id
    
    def clean_start_date(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        start_date = self.cleaned_data.get("start_date")
        if not re.match(r"\d{2}\.\d{2}\.\d{4}$", start_date) or not check_date(start_date):
            raise ValidationError("Дата начала работ введена некорректно.")
        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y")
        if Employee.objects.filter(id = employee_id).exists():
            if Schedule.objects.exclude(id=self.id).filter(Q(employee__id=employee_id) & Q(start_date__lte=start_date) & Q(end_date__gte=start_date)).exists():
                raise ValidationError("Данный сотрудник занят в указанный промежуток времени (некорректная дата начала)")
        if Machine.objects.filter(id = machine_id).exists():
            if Schedule.objects.exclude(id=self.id).filter(Q(machine__id=machine_id) & Q(start_date__lte=start_date) & Q(end_date__gte=start_date)).exists():
                raise ValidationError("Данный станок занят в указанный промежуток времени (некорректная дата начала)")
        return start_date
    
    def clean_end_date(self):
        machine_id = self.cleaned_data.get("machine_id")
        employee_id = self.cleaned_data.get("employee_id")
        end_date = self.cleaned_data.get("end_date")
        if not re.match(r"\d{2}\.\d{2}\.\d{4}$", end_date) or not check_date(end_date):
            raise ValidationError("Дата окончания работ введена некорректно.")
        end_date = datetime.datetime.strptime(end_date, "%d.%m.%Y")
        start_date = self.cleaned_data.get("start_date")
        if start_date is not None:
            if end_date < start_date:
                raise ValidationError("Дата окончания не может быть раньше даты начала")
            if Employee.objects.filter(id = employee_id).exists():
                if Schedule.objects.exclude(id=self.id).filter(Q(employee__id=employee_id) & Q(start_date__lte=end_date) & Q(end_date__gte=end_date)).exists():
                    raise ValidationError("Данный сотрудник занят в указанный промежуток времени (некорректная дата окончания)")
                elif Schedule.objects.exclude(id=self.id).filter(Q(employee__id=employee_id) & Q(start_date__gte=start_date) & Q(end_date__lte=end_date)).exists():
                    raise ValidationError("Данный сотрудник занят в указанный промежуток времени")
            if Machine.objects.filter(id = machine_id).exists():
                if Schedule.objects.exclude(id=self.id).filter(Q(machine__id=machine_id) & Q(start_date__lte=end_date) & Q(end_date__gte=end_date)).exists():
                    raise ValidationError("Данный станок занят в указанный промежуток времени (некорректная дата окончания)")
                elif Schedule.objects.exclude(id=self.id).filter(Q(machine__id=machine_id) & Q(start_date__gte=start_date) & Q(end_date__lte=end_date)).exists():
                    raise ValidationError("Данный станок занят в указанный промежуток времени")
        return end_date
    
    def save(self, commit=True):
        schedule_item =  Schedule.objects.get(id=self.id)
        schedule_item.order = Order.objects.get(id=self.cleaned_data.get("order_id"))
        schedule_item.employee = Employee.objects.get(id=self.cleaned_data.get("employee_id"))
        schedule_item.machine = Machine.objects.get(id=self.cleaned_data.get("machine_id"))
        schedule_item.start_date = self.cleaned_data.get("start_date")
        schedule_item.end_date = self.cleaned_data.get("end_date")
        if commit:
            schedule_item.save()
        return schedule_item       


# ----------------------- Месячные расходы -----------------------

class MonthlySpendingsSearchForm(forms.Form):
    CHOICES = (
        ("month", "по месяцу"),
        ("month_interval", "по временному промежутку"),
        ("total_cost", "сумме трат"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "month":
                if not re.match(r"\d{2}\.\d{4}$", value) or not check_date("01." + value):
                    raise ValidationError("Месяц введён некорректно.")
        return value
    
    def clean_interval_start(self):
        search_column = self.cleaned_data.get("search_column")
        start_value = self.cleaned_data.get("interval_start")
        if search_column == "month_interval":
            if start_value is not None and start_value:
                if not re.match(r"\d{2}\.\d{4}$", start_value) or not check_date("01." + start_value):
                    raise ValidationError("Начальная дата введена некорректно.")
            else:
                start_value = "01.0001"
        elif search_column == "total_cost":
            if start_value is not None and start_value:
                if not re.match(r"\d+$" , start_value):
                    raise ValidationError("Начальная сумма введена некорректно.")
            else:
                start_value = "0"
        return start_value
    
    def clean_interval_end(self):
        search_column = self.cleaned_data.get("search_column")
        end_value = self.cleaned_data.get("interval_end")
        if search_column == "month_interval":
            if end_value is not None and end_value:
                if not re.match(r"\d{2}\.\d{4}$", end_value) or not check_date("01." + end_value):
                    raise ValidationError("Конечная дата введена некорректно.")
            else:
                end_value = "12.9999"
        if search_column == "total_cost":
            if end_value is not None and end_value:
                if not re.match(r"\d+$" , end_value):
                    raise ValidationError("Конечная сумма введена некорректно.")
            else:
                end_value = "2147483646"
        return end_value
    

# ----------------------- Пользователи -----------------------


class UserSearchForm(forms.Form):
    CHOICES = (
        ("username", "по имени пользователя"),
        ("role", "по роли"),
    )
    search_column = forms.ChoiceField(choices=CHOICES)
    common_text = forms.CharField(required=False)
    interval_start = forms.CharField(required=False)
    interval_end = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search_column'].widget.attrs.update({'id': 'search-options', 'class': 'search-input-selector'})
        self.fields['common_text'].widget.attrs.update({'id': 'text-input','class': 'search-input-field'})
        self.fields['interval_start'].widget.attrs.update({'id': 'interval-start-input', 'class': 'search-input-field'})
        self.fields['interval_end'].widget.attrs.update({'id': 'interval-end-input', 'class': 'search-input-field'})

    def clean_common_text(self):
        search_column = self.cleaned_data.get("search_column")
        value = self.cleaned_data.get("common_text")
        if value is not None and value:
            if search_column == "role":
                if not re.match(r"\w+$", value):
                    raise ValidationError("Некорректно введено название роли пользователя")
        return value
    

class UserCreateForm(forms.ModelForm):
    CHOICES = (
        ("Manager", "Manager"),
        ("PurchaseDepartment", "PurchaseDepartment"),
        ("Chief", "Chief"),
        ("Admin", "Admin"),
    )
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль")
    role = forms.ChoiceField(label="Роль", choices=CHOICES)


    class Meta:
        model = User
        fields = ["username"]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['password'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['role'].widget.attrs.update({'class': 'select-field input-field'})


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Имя уже занято")
        return username


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name=self.cleaned_data.get("role")))
            user.save()
        return user


class UserEditForm(forms.Form):
    CHOICES = (
        ("Manager", "Manager"),
        ("PurchaseDepartment", "PurchaseDepartment"),
        ("Chief", "Chief"),
        ("Admin", "Admin"),
    )
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", required=False)
    role = forms.ChoiceField(label="Роль", choices=CHOICES)
    

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop("id", None)
        if kwargs.get("initial") is not None:
            kwargs["initial"]["password"] = None
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['password'].widget.attrs.update({'class': 'common-field input-field'})
        self.fields['role'].widget.attrs.update({'class': 'select-field input-field'})
        role = User.objects.get(id=self.id).groups.all()[0]
        self.fields['role'].initial = role


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(id=self.id).filter(username=username).exists():
            raise ValidationError("Имя уже занято")
        return username


    def save(self, commit=True):
        user = User.objects.get(id=self.id)
        password = self.cleaned_data.get("password")
        if password != None and password:
            user.set_password(password)
        user.username = self.cleaned_data.get("username")
        user.groups.clear()
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name=self.cleaned_data.get("role")))
            user.save()
        return user   