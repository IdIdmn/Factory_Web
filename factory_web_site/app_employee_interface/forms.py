import re
from django import forms
from django.forms import ValidationError
from django.db.models import Q
from app_client_interface.models import *


class OrderSearchForm(forms.Form):
    CHOICES = (
    ("email", "почтовому адресу"),
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
                if not re.match(r"[ а-яА-ЯёЁa-zA-Z]+$", value):
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
    

class OrderCreateEditForm(forms.ModelForm):
    CHOICES = (
    ("Ремонт", "Ремонт"),
    ("Создание детали по чертежам", "Создание детали по чертежам"),
    ("Создание детали с нуля", "Создание детали с нуля")
    )
    email = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    order_type = forms.ChoiceField( choices=CHOICES)
    cost = forms.CharField()
    files = forms.FileField(required=False)





# class MultipleDeleteForm(forms.Form):
    
#     def __init__(self, *args, **kwargs): 
#         options = kwargs.pop('options', []) 
#         super(MultipleDeleteForm, self).__init__(*args, **kwargs)
#         for option in options:
#             self.fields[option] = forms.BooleanField(required=False)
#             self.fields[option].widget.attrs.update({'class': 'delete-checkbox'})

