from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    email = models.CharField(max_length=50)
    description = models.TextField(null = True, blank = True)
    order_type = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to="projects_store", blank=True, null=True)


class Client(models.Model):
    user = models.OneToOneField(User, related_name = "client_info", on_delete = models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)


    