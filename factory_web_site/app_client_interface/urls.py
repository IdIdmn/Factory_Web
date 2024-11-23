from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path('', main_page, name="home_page"),
    path('profile', client_profile, name="client_profile"),
    path('profile/edit', edit_profile, name="edit_profile"),
]