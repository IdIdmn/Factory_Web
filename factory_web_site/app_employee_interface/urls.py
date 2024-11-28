from django.urls import path
from .views import *

app_name = "employee"

urlpatterns = [
    path('orders/', orders_list, name="order-list"),
    path('sort_by/<sort_by_column>/<sort_direction>/', sort_table, name="sort_by"),
    path('reset_table/', reset_table, name="reset_table"),
]