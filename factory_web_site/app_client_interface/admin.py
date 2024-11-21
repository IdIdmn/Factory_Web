from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Order)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('email', 'description', "order_type", "date", "files")
    search_fields = ('email', "order_type", "date",)
    date_hierarchy = 'date'


@admin.register(Client)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone_number")
    search_fields = ("full_name", "email", "phone_number")