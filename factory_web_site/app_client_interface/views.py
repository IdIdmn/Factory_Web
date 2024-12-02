from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import model_to_dict
from .models import *
from .forms import *
import datetime
from django.db.models import Sum
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required


def change_direction(sort_direction):
    if sort_direction == "desc" or sort_direction is None:
        return "asc"
    else:
        return "desc"


def is_Manager(user):
    return user.groups.filter(name='Manager').exists()


def is_PurchaseDepartmentEmployee(user):
    return user.groups.filter(name='PurchaseDepartment').exists()


def is_Chief(user):
    return user.groups.filter(name='Chief').exists()


def is_Client(user):
    return user.groups.filter(name='Client').exists()


def is_Employee(user):
    return is_Manager(user) or is_Chief(user) or is_PurchaseDepartmentEmployee(user)


def main_page(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/#connect-with-us-section")
        else:
            request.session['form_data'] = request.POST
            if request.FILES.get('files') is not None:
                request.session['filename'] = request.FILES.get('files').name
            return redirect("/#connect-with-us-section")
    else:
        form_data = request.session.pop('form_data', None)
        file_name = request.session.pop('filename', None)
        current_user = request.user
        if form_data is not None:
            form = OrderForm(form_data, filename = file_name, user = current_user)
        else:
            form = OrderForm(user = current_user)
        employee_url = ""
        if is_Employee(current_user):
            if is_Manager(current_user):
                employee_url = reverse("employee:orders")
            elif is_Chief(current_user):
                employee_url = reverse("employee:employees")
            elif is_PurchaseDepartmentEmployee(current_user):
                employee_url = reverse("employee:vendors")
        context = {
            'form': form, 
            'title': "МОЗ №1",
            "is_employee": is_Employee(request.user), 
            "is_client": is_Client(request.user),
            "is_Manager": is_Manager(request.user),
            "is_Chief": is_Chief(request.user),
            "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
            "employee_url" : employee_url
        }
    return render(request, "MainPage.html", context)


@login_required(login_url="log_reg:sign_in")
def client_profile(request):
    if request.method == 'POST':
        form = OrderSearchForm(request.POST)
        search_params = request.GET.copy()
        if form.is_valid():
            search_column = form.cleaned_data.get("search_column")
            if search_column == "date_interval" or search_column == "cost":
                interval_borders = [form.cleaned_data.get("interval_start"), form.cleaned_data.get("interval_end")]
                search_params[search_column] = ", ".join(interval_borders)
            else:
                search_params[search_column] = form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(search_params) + "#orders_table")
        else: 
            request.session['form_data'] = request.POST
            if search_params:
                return redirect(request.path + "?" + urlencode(search_params) + "#orders_table")
            else:
                return redirect(request.path + "#orders_table")
    else:
        sort_by_column = request.session.pop('sort_by_column', None)
        sort_direction = request.session.pop('sort_direction', None)
        form_data = request.session.pop('form_data', None)
        # переносим данные, если в прошлой форме были допущены ошибки
        if form_data is None:
            form = OrderSearchForm()
        else:
            form = OrderSearchForm(form_data)
        search_params = request.GET.copy()
        user_orders = request.user.client_info.orders.all().order_by("id")
        # если есть что искать - ищем
        empty_table_phrase = "Вы ещё не оформляли заказов."
        if search_params:
            user_orders = user_orders.find(search_params)
        if user_orders.count() == 0:
            empty_table_phrase = "Нет заказов, удовлетворяющих заданным условиям."
        # если есть что сортировать - сортируем
        if sort_by_column is not None:
            user_orders = user_orders.sort(sort_by_column, sort_direction)
        # считаем общие характеристики таблицы
        total_spendings = user_orders.filter(cost__isnull=False).aggregate(total=Sum('cost'))['total']
        if total_spendings is None:
            total_spendings = 0
        # находим параметры нынешнего url-адреса
        if search_params:
            current_params ="?" + urlencode(search_params)
        else:
            current_params = ""
            context = {
                'title': "Профиль", 
                "current_params": current_params, 
                "empty_table_phrase": empty_table_phrase, 
                "form": form , 
                'total_spendings' : total_spendings, 
                "user_orders": user_orders,
                "sort_direction": change_direction(sort_direction) , 
                'model_field_titles': Order.get_fields_titles_ru_en_dict(), 
                "table_column_titles": Order.get_profile_order_list_titles()
            }
        return render(request, "client-profile.html", context)


@login_required(login_url="log_reg:sign_in")
def sort_orders(request, sort_by_column, sort_direction):
    if sort_direction == "desc" and request.session.pop('previous_sorted_column', None) != f"{sort_by_column}":
        sort_direction = "asc"
    request.session['sort_by_column'] = sort_by_column
    request.session['sort_direction'] = sort_direction
    request.session['previous_sorted_column'] = f"{sort_by_column}"
    request_params = request.GET.copy()
    return redirect(reverse("main:client_profile") + "?" + urlencode(request_params) + "#orders_table")


@login_required(login_url="log_reg:sign_in")
def edit_profile(request):
    if request.method == "POST":
        form = ClientEditForm(request.POST, email = request.user.client_info.email)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:client_profile"))
    else:
        form = ClientEditForm(initial=model_to_dict(request.user.client_info), email = request.user.client_info.email)
    return render(request, "edit-profile.html", {'title': "Изменение профиля", 'form': form})


@login_required(login_url="log_reg:sign_in")
def reset_profile(request):
    return redirect(reverse("main:client_profile") + "#orders_table")
