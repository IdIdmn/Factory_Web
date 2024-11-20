from django.db import models


class Order(models.Model):
    email = models.CharField(max_length = 50)
    description = models.TextField(null = True, blank = True)
    order_type = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to="projects_store", blank=True, null=True)