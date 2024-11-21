from django.urls import path, include
from .views import *

app_name = "log_reg"

urlpatterns = [
    path('sign_up/', sign_up, name="sign_up"),
    path('sign_in/', sign_in, name="sign_in"),
]
