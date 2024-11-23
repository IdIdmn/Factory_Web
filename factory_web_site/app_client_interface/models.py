from tkinter import CASCADE
from turtle import st
from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    email = models.CharField(max_length=50)
    user = models.OneToOneField(User, related_name = "client_info", on_delete = models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True,null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

class Order(models.Model):
    client = models.ForeignKey(Client, related_name="orders", on_delete=models.CASCADE, null=True)
    description = models.TextField(null = True, blank = True)
    order_type = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField(blank=True, null=True)
    files = models.FileField(upload_to="projects_store", blank=True, null=True)

    @staticmethod
    def get_profile_order_list_titles():
        return ["Тип заказа", "Комментарий", "Дата", "Цена", "Файл проекта"]

    @staticmethod
    def get_fields_values_titles():
        return ["Почта клиента", "Комментарий", "Тип заказа", "Дата", "Цена", "Файл проекта"]

    @property
    def profile_order_list(self):
        return [self.order_type, self.description, self.date, self.cost]

    @property
    def fields_values(self):
        return [self.client.email, self.description, self.order_type, self.date, self.cost]