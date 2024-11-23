from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Order)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('client','description', "order_type", "date", "files")
    search_fields = ('client',"order_type", "date",)
    date_hierarchy = 'date'


@admin.register(Client)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("user","email", "full_name", "phone_number")
    search_fields = ("user","email", "full_name", "phone_number")