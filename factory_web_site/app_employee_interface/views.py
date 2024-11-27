from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from app_client_interface.models import *


def is_in_group(user);
    return user.groups.filter(name='your_group_name').exists()


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_in_group, login_url="log_reg:sign_in")
def orders_list(request):
    return render(request, "table-page.html", {"table": Order.objects.all(), "table_column_titles": Order.get})