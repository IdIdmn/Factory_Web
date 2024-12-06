from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Supply)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'order','material', "date", "quantity", "cost")
