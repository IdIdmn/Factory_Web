from django.urls import path, include
from .views import *

app_name = "log_reg"

urlpatterns = [
    path('login/', login_user, name="login"),
]
