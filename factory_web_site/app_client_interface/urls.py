from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path('', main_page, name="home_page"),
    path('client/profile/', client_profile, name="client_profile"),
    path('client/profile/edit/', edit_profile, name="edit_profile"),
    path('client/profile/reset/', reset_profile, name="reset_profile"),
    path('client/profile/sort_orders_by/<sort_by_column>/<sort_direction>/', sort_orders, name="sort_by"),
]