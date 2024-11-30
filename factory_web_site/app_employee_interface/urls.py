from django.urls import path
from .views import *

app_name = "employee"

urlpatterns = [
    path('orders/', orders_list, name="orders"),
    path('clients/', clients_list, name="clients"),
    path('vendors/', vendors_list, name="vendors"),
    path('employees/', employees_list, name="employees"),
    path('machines/', machines_list, name="machines"),
    path('supplies/', supplies_list, name="supplies"),
    path('materials/', materials_list, name="materials"),
    path('schedule/', schedule, name="schedule"),
    path('sort_by/<model>/<sort_by_column>/<sort_direction>/', sort_table, name="sort_by"),
    path('reset_table/', reset_table, name="reset_table"),
    path('delete/<model_name>/<item_id>/<row>/', delete_item, name="delete_item"),
    path('edit/<model_name>/<item_id>/<row>/', edit_item, name="edit_item"),
    path('create/<model_name>/', create_item, name="create_item"),
]