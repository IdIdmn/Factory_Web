from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path('', main_page, name="home_page"),
    path('profile/', client_profile, name="client_profile"),
    path('profile/edit/', edit_profile, name="edit_profile"),
    path('profile/reset/', reset_profile, name="reset_profile"),
    path('profile/sort_orders_by/<sort_by_column>/<sort_direction>/', sort_orders, name="sort_by"),
]