from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_client_interface.urls',  namespace="main")),
    path('', include('app_log_reg_form.urls',  namespace="log_reg"))
]
