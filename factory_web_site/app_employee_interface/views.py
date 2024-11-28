from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from app_client_interface.models import Order
from .forms import *
import datetime
from django.shortcuts import get_object_or_404


def is_Manager(user):
    return user.groups.filter(name='Manager').exists()


def change_direction(sort_direction):
    if sort_direction == "desc" or sort_direction is None:
        return "asc"
    else:
        return "desc"

@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def orders_list(request):
    if request.method == 'POST':
        search_form = OrderSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "date_interval" or search_column == "cost":
                interval_borders = [search_form.cleaned_data.get("interval_start"), search_form.cleaned_data.get("interval_end")]
                request_params[search_column] = ", ".join(interval_borders)
            else:
                request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        search_form = OrderSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список заказов пуст"        
    orders = Order.objects.all()
    if request_params:
        order_type = request_params.get("order_type", None)
        date = request_params.get("date", None)
        date_interval_borders = request_params.get("date_interval", None)
        cost_interval_borders = request_params.get("cost", None)
        email = request_params.get("email", None)
        if email is not None and email:
            orders = orders.find_by_client_email(email, include=True)
        if date_interval_borders is not None:
            date_interval_borders = date_interval_borders.split(", ")
            orders = orders.find_by_date_interval(datetime.datetime.strptime(date_interval_borders[0], "%d.%m.%Y"), datetime.datetime.strptime(date_interval_borders[1], "%d.%m.%Y"))
        if order_type is not None and order_type:
            orders = orders.find_by_order_type(order_type, include = True)
        if date is not None and date:
            orders = orders.find_by_date(datetime.datetime.strptime(date, "%d.%m.%Y"))
        if cost_interval_borders is not None:
            cost_interval_borders = cost_interval_borders.split(", ")
            orders = orders.find_by_cost_interval(int(cost_interval_borders[0]), int(cost_interval_borders[1]))
        if orders.count() == 0:
            empty_table_phrase = "Нет заказов, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        if sort_direction == "desc":
            sort_by_column = "-" + sort_by_column
        orders = orders.order_by(sort_by_column)
    if request_params:
        request_params ="?" + urlencode(request_params)
    # options = [id for id in orders.values_list('id', flat=True)]
    # delete_form = MultipleDeleteForm(options = options)
    context = {"search_form": search_form,
                # "delete_form" : delete_form,
                "model_name": "Order",
                "title": "Список заказов",
                "model": orders, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Order.get_fields_values_titles(), 
                "model_field_titles":Order.get_fields_titles_ru_en_dict()}
    return render(request, "table-page.html", context)

@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def sort_table(request, sort_by_column, sort_direction):
    request.session['sort_by_column'] = sort_by_column
    request.session['sort_direction'] = sort_direction
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    return redirect(previous_url + "?" + urlencode(request_params) + "#orders_table")


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def reset_table(request):
    request_params = request.GET.copy()
    return redirect(request_params.pop("url")[0])

@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def delete_item(request, model_name, item_id, row):
    models = {"Order": Order, "Client": Client}
    object = get_object_or_404(models[model_name], id=item_id)
    object.delete()
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    return redirect(previous_url + "?" + urlencode(request_params) + f"#table-row-{int(row) - 1}")
