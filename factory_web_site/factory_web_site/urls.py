from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_client_interface.urls',  namespace="main")),
    path('', include('app_log_reg_form.urls',  namespace="log_reg")),
    path('employee/', include('app_employee_interface.urls',  namespace="employee")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
