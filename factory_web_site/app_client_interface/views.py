from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import model_to_dict
from .models import *
from .forms import *
import datetime
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required


def change_direction(sort_direction):
    if sort_direction == "desc" or sort_direction is None:
        return "asc"
    else:
        return "desc"


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
        if form_data is not None:
            form = OrderForm(form_data, filename = file_name, user = request.user)
        else:
            form = OrderForm(user = request.user)
    return render(request, "MainPage.html", {'form': form, 'title': "МОЗ №1"})


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
        user_orders = request.user.client_info.orders.all()
        # если есть что искать - ищем
        empty_table_phrase = "Вы ещё не оформляли заказов."
        if search_params:
            order_type = search_params.get("order_type", None)
            date = search_params.get("date", None)
            date_interval_borders = search_params.get("date_interval", None)
            cost_interval_borders = search_params.get("cost", None)
            if date_interval_borders is not None:
                date_interval_borders = date_interval_borders.split(", ")
                user_orders = user_orders.find_by_date_interval(datetime.datetime.strptime(date_interval_borders[0], "%d.%m.%Y"), datetime.datetime.strptime(date_interval_borders[1], "%d.%m.%Y"))
            if order_type is not None and order_type:
                user_orders = user_orders.find_by_order_type(order_type, include = True)
            if date is not None and date:
                user_orders = user_orders.find_by_date(datetime.datetime.strptime(date, "%d.%m.%Y"))
            if cost_interval_borders is not None:
                cost_interval_borders = cost_interval_borders.split(", ")
                user_orders = user_orders.find_by_cost_interval(int(cost_interval_borders[0]), int(cost_interval_borders[1]))
            if user_orders.count() == 0:
                empty_table_phrase = "Нет заказов, удовлетворяющих заданным условиям."
        # если есть что сортировать - сортируем
        if sort_by_column is not None:
            user_orders = user_orders.sort_orders(sort_by_column, sort_direction)
        # считаем общие характеристики таблицы
        total_spendings = user_orders.filter(cost__isnull=False).aggregate(total=Sum('cost'))['total']
        if total_spendings is None:
            total_spendings = 0
        # находим параметры нынешнего url-адреса
        if search_params:
            current_params ="?" + urlencode(search_params)
        else:
            current_params = ""
        return render(request, "client-profile.html", {'title': "Профиль", "current_params": current_params, "empty_table_phrase": empty_table_phrase, "form": form , 'total_spendings' : total_spendings, "user_orders": user_orders,
        "sort_direction": change_direction(sort_direction) , 'model_field_titles': Order.get_fields_titles_ru_en_dict(), "table_column_titles": Order.get_profile_order_list_titles()})


@login_required(login_url="log_reg:sign_in")
def sort_orders(request, sort_by_column, sort_direction):
    request.session['sort_by_column'] = sort_by_column
    request.session['sort_direction'] = sort_direction
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
