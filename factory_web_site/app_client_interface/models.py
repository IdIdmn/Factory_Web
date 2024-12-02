from django.db import models
from django.contrib.auth.models import User
from .managers import *
import os


class Client(models.Model):
    email = models.CharField(max_length=50)
    user = models.OneToOneField(User, related_name = "client_info", on_delete = models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True,null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    objects = ClientManager()

    class Meta:
        ordering = ["email"]

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "Почта клиента": "email" ,"Полное имя": "full_name", "Номер телефона": "phone_number"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID","Почта клиента", "Полное имя", "Номер телефона"]
    
    @property
    def fields_values(self):
        return [self.id, self.email, self.full_name, self.phone_number]
     

class Order(models.Model):
    client = models.ForeignKey(Client, related_name="orders", on_delete=models.CASCADE, null=True)
    description = models.TextField(null = True, blank = True)
    order_type = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    cost = models.FloatField(blank=True, null=True)
    files = models.FileField(upload_to="projects_store", blank=True, null=True)
    status = models.CharField(default="На рассмотрении")

    objects = OrderManager()

    def delete(self, *args, **kwargs):
        if self.files: 
            if os.path.isfile(self.files.path):
                os.remove(self.files.path)
        super(Order, self).delete(*args, **kwargs)

    @property
    def filename(self):
        return str(self.files)[str(self.files).rfind('/') + 1:]

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "Почта клиента": "client" ,"Тип заказа": "order_type", "Комментарий": "description", "Дата": "date", "Статус": "status",  "Цена, руб.": "cost", "Файл проекта": "files"}

    @staticmethod 
    def get_profile_order_list_titles():
        return ["Тип заказа", "Комментарий", "Дата", "Статус", "Цена, руб.", "Файл проекта"]

    @staticmethod
    def get_fields_values_titles():
        return ["ID", "Почта клиента", "Комментарий", "Тип заказа", "Дата", "Статус", "Цена, руб.", "Файл проекта"]

    @property
    def profile_order_list(self):
        return [self.order_type, self.description, self.date, self.status, self.cost]

    @property
    def fields_values(self):
        return [self.id, self.client.email, self.description, self.order_type, self.date, self.status, self.cost, self.files]