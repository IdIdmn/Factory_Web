from django.urls import path
from .views import *

app_name = "employee"

urlpatterns = [
    # model tables
    path('orders/', orders_list, name="orders"),
    path('clients/', clients_list, name="clients"),
    path('vendors/', vendors_list, name="vendors"),
    path('employees/', employees_list, name="employees"),
    path('machines/', machines_list, name="machines"),
    path('supplies/', supplies_list, name="supplies"),
    path('materials/', materials_list, name="materials"),
    path('schedule/', schedule, name="schedule"),
    path('users/', users_list, name="users"),
    # sort by column
    path('sort_by/<model_name>/<sort_by_column>/<sort_direction>/', sort_table, name="sort_by"),
    # reset search query
    path('reset_table/', reset_table, name="reset_table"),
    # confirm and cancel confirm order
    path('confirm_order/<item_id>/<row>/', confirm_order, name="confirm_order"),
    path('cancel_confirm_order/<item_id>/<row>/', cancel_order_confirm, name="cancel_order_confirm"),
    # delete
    path('delete/<model_name>/<item_id>/<row>/', delete_item, name="delete_item"),
    # cdit
    path('edit/<model_name>/<edit_item_id>/<edit_item_row>/', edit_item, name="edit_item"),
    path('edit/<model_name>/<edit_item_id>/<edit_item_row>/<chosen_model_name>/<chosen_item_id>/', edit_item, name="edit_chosen_item"),
    # create
    path('create/<model_name>/', create_item, name="create_item"),
    path('create/<model_name>/<chosen_model_name>/<chosen_item_id>/', create_item, name="create_chosen_item"),
    # choose
    path('choose_item/<form_model_name>/<chosen_model_name>/<form_type>/', choose_item, name="choose_item_to_create"),
    path('choose_item/<form_model_name>/<chosen_model_name>/<form_type>/<edit_item_id>/<edit_item_row>', choose_item, name="choose_item_to_edit"),
    # order_info
    path('orders/order_info/<order_id>/<row>/', order_info, name="order_info"),
    # monthly_spendings
    path('supplies/monthly_spendings/', monthly_spendings, name="monthly_spendings"),
]