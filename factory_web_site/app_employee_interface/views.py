from urllib.parse import urlencode
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from app_client_interface.models import Order
from .forms import *
from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth
from django.db.models import Sum 
from django.contrib.auth.models import User

ITEM_EDIT_FORMS = {"Order": OrderEditForm, "Client": ClientEditForm, "Vendor": VendorEditForm, "Material": MaterialEditForm, "Employee": EmployeeEditForm,
                        "Machine": MachineEditForm, "Supply": SupplyEditForm, "Schedule": ScheduleEditForm, "User": UserEditForm}

ITEM_CREATE_FORMS = {"Order": OrderCreateForm, "Vendor": VendorCreateForm, "Material": MaterialCreateForm,  "Employee": EmployeeCreateForm, "Machine": MachineCreateForm,
                        "Supply": SupplyCreateForm, "Schedule": ScheduleCreateForm, "User": UserCreateForm}

MODELS = {"Order": Order, "Client": Client, "Vendor": Vendor, "Material":Material, "Employee": Employee, "Machine": Machine, "Supply": Supply, "Schedule": Schedule, "User": User}

OBJECT_TYPES = {"Order": "о заказе", "Client": "о клиенте", "Vendor": "о поставщике", "Material": "о материале" , "Employee": "о сотруднике", "Machine": "о станке",
                    "Supply": "о поставке", "Schedule": "о записи в графике занятости", "User": "о пользователе"}

ITEM_SEARCH_FORMS = {"Order": OrderSearchForm, "Material": MaterialSearchForm, "Employee": EmployeeSearchForm, "Machine": MachineSearchForm}

CHOOSE_TABLE_NAME = {"Order": "Выбор заказа", "Material": "Выбор материала", "Employee": "Выбор сотрудника", "Machine": "Выбор станка"}

ALLOWED_MODELS = { 'Manager': ['Order', 'Client'], 'Chief': ['Employee', "Machine", "Schedule"], 'PurchaseDepartment': ['Vendor', 'Material', "Supply"], "Admin": ["User"] } 

MONTHS = { 'January': 'Январь', 'February': 'Февраль', 'March': 'Март', 'April': 'Апрель', 'May': 'Май', 'June': 'Июнь', 'July': 'Июль',
           'August': 'Август', 'September': 'Сентябрь', 'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь'
}


def has_permission_to_modify(user, model_name):
    if is_Superuser(user):
        return True
    elif is_Manager(user):
        return model_name in ALLOWED_MODELS['Manager']
    elif is_Chief(user):
        return model_name in ALLOWED_MODELS['Chief'] 
    elif is_PurchaseDepartmentEmployee(user):
        return model_name in ALLOWED_MODELS['PurchaseDepartment']


def is_Manager(user):
    return user.groups.filter(name='Manager').exists()


def is_PurchaseDepartmentEmployee(user):
    return user.groups.filter(name='PurchaseDepartment').exists()


def is_Chief(user):
    return user.groups.filter(name='Chief').exists()


def is_Employee(user):
    return is_Manager(user) or is_PurchaseDepartmentEmployee(user) or is_Chief(user) or is_Admin(user)


def is_Superuser(user):
    return is_Manager(user) and is_PurchaseDepartmentEmployee(user) and is_Chief(user) and is_Admin(user)


def is_Admin(user):
    return user.groups.filter(name='Admin').exists()


def change_search_items_status(search_column, request_params):
    if search_column == "unprocessed_applications":
        request_params.pop("processed_applications", None)
        request_params.pop("in_work", None)
        request_params.pop("executed", None)
    elif search_column == "processed_applications":
        request_params.pop("unprocessed_applications", None)
        request_params.pop("in_work", None)
        request_params.pop("executed", None)
    elif search_column == "in_work":
        request_params.pop("unprocessed_applications", None)
        request_params.pop("executed", None)
    elif search_column == "executed":
        request_params.pop("unprocessed_applications", None)
        request_params.pop("in_work", None)


def change_direction(sort_direction):
    if sort_direction == "desc" or sort_direction is None:
        return "asc"
    else:
        return "desc"


def merge_initial(initial, item_params):
    temp = initial.copy()
    for key in item_params.keys():
        if f"{key}_id" in temp:
            if temp[f"{key}_id"] is None:
                temp[f"{key}_id"] = item_params[key]
        else:
            if key.endswith("date"):
                temp[key] = datetime.date.strftime(item_params[key], "%d.%m.%Y")
            else:
                temp[key] = item_params[key]
    return temp


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def sort_table(request, model_name, sort_by_column, sort_direction):
    if sort_direction == "desc" and request.session.pop('previous_sorted_model', None) != f"{model_name}-{sort_by_column}":
        sort_direction = "asc"
    request.session['sort_direction'] = sort_direction
    request.session['sort_by_column'] = sort_by_column
    request.session['previous_sorted_model'] = f"{model_name}-{sort_by_column}"
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url = previous_url + "?" + urlencode(request_params)
    return redirect(previous_url)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def reset_table(request):
    request.session.pop('form_data', None)
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    pre_form_url = request_params.pop("pre-form-url", None)
    request_params.clear()
    if pre_form_url is not None:
        request_params["pre-form-url"] = pre_form_url[0]
        previous_url = previous_url + "?" + urlencode(request_params)
    return redirect(previous_url)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def delete_item(request, model_name, item_id, row):
    if not has_permission_to_modify(request.user, model_name):
        return redirect(reverse("log_reg:sign_in"))
    object = get_object_or_404(MODELS[model_name], id=item_id)
    object.delete()
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url += "?" + urlencode(request_params) 
    previous_url += f"#table-row-{int(row) - 1}"
    return redirect(previous_url)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def create_item(request, model_name, chosen_model_name=None, chosen_item_id=None):
    if not has_permission_to_modify(request.user, model_name):
        return redirect(reverse("log_reg:sign_in"))
    request_params = request.GET.copy()
    # Выбираем url, по которму возвращаться в исходную таблицу
    # Если произведён выбор модели до достаём из request_params "pre-form-url", так как простой "url" переопределяли в окне выбора
    if chosen_model_name is not None and chosen_item_id is not None:
        previous_url = request_params.pop("pre-form-url")[0]
        request_params.clear()
        if request_params:
            previous_url = previous_url + "?" + urlencode(request_params)
    # В ином же случае просто проходим по url
    else:
        previous_url = request_params.pop("url")[0]
        if request_params:
            previous_url = previous_url + "?" + urlencode(request_params)
    # Переходим к обработке самого запроса запроса
    if request.method == "POST":
        form = ITEM_CREATE_FORMS[model_name](request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(previous_url)
    else:
        if chosen_model_name is not None and chosen_item_id is not None:
            if model_name == "Supply":
                initial_form_data = request.session.pop("initial_form_data", {"order_id":  None, "material_id": None, })
            elif model_name == "Schedule":
                initial_form_data = request.session.pop("initial_form_data", {"order_id": None, "employee_id": None, "machine_id": None})
            initial_form_data[f"{chosen_model_name.lower()}_id"] = chosen_item_id
            request.session["initial_form_data"] = initial_form_data
            form = ITEM_CREATE_FORMS[model_name](initial=initial_form_data)
        else:
            request.session.pop("initial_form_data", None)
            form = ITEM_CREATE_FORMS[model_name]()
    context = {
        "form": form, 
        "title": "Редактирование", 
        "previous_url" : previous_url, 
        "object_type": OBJECT_TYPES[model_name]}
    if model_name == "Supply" or model_name == "Schedule":
        context["form_model_name"] = model_name
        context["form_type"] = "create"
        request_params.clear()
        request_params["pre-form-url"] = previous_url
        context["request_params"] = "?" + urlencode(request_params)
        return render(request, "expanded-add-edit-page.html", context)
    else:
        return render(request, "add-edit-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def edit_item(request, model_name, edit_item_id, edit_item_row, chosen_model_name=None, chosen_item_id=None):
    if not has_permission_to_modify(request.user, model_name):
        return redirect(reverse("log_reg:sign_in"))
    request_params = request.GET.copy()
    # Выбираем url, по которму возвращаться в исходную таблицу
    # Если произведён выбор модели до достаём из request_params "pre-form-url", так как простой "url" переопределяли в окне выбора
    if chosen_model_name is not None and chosen_item_id is not None:
        previous_url = request_params.pop("pre-form-url")[0]
        request_params.clear()
        if request_params:
            previous_url += "?" + urlencode(request_params)
    # В ином же случае просто проходим по url
    else:
        previous_url = request_params.pop("url")[0]
        if request_params:
            previous_url += "?" + urlencode(request_params)
    # Задаём номер ряда, к которому нужно будет перемотать страницу по возвращении
    if "#" not in previous_url:
        previous_url += f"#table-row-{int(edit_item_row) - 1}"
    # Переходим к обработке самого запроса запроса
    if request.method == "POST":
        form = ITEM_EDIT_FORMS[model_name](request.POST, id = edit_item_id)
        if form.is_valid():
            form.save()
            return redirect(previous_url)
    else:
        item = get_object_or_404(MODELS[model_name], id=edit_item_id)
        item_params = model_to_dict(item)
        if chosen_model_name is not None and chosen_item_id is not None:
            if model_name == "Supply":
                initial_form_data = request.session.pop("initial_form_data", {"order_id":  None, "material_id": None, })
            elif model_name == "Schedule":
                initial_form_data = request.session.pop("initial_form_data", {"order_id": None, "employee_id": None, "machine_id": None})
            initial_form_data[f"{chosen_model_name.lower()}_id"] = chosen_item_id
            initial_form_data = merge_initial(initial_form_data, item_params)
            request.session["initial_form_data"] = initial_form_data
            form = ITEM_CREATE_FORMS[model_name](initial=initial_form_data)
        else:
            request.session.pop("initial_form_data", None)
            form = ITEM_EDIT_FORMS[model_name](initial=item_params, id = edit_item_id)
    context = {
        "form": form,
        "title": "Редактирование", 
        "previous_url" : previous_url, 
        "object_type": OBJECT_TYPES[model_name]
    }
    if model_name == "Supply" or model_name == "Schedule":
        context["form_model_name"] = model_name
        context["form_type"] = "edit"
        context["edit_item_id"] = edit_item_id
        context["edit_item_row"] = edit_item_row
        request_params.clear()
        request_params["pre-form-url"] = previous_url
        context["request_params"] = "?" + urlencode(request_params)
        return render(request, "expanded-add-edit-page.html", context)
    else:
        return render(request, "add-edit-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(lambda user: is_Chief(user) or is_PurchaseDepartmentEmployee(user), login_url="log_reg:sign_in")
def choose_item(request, form_model_name, chosen_model_name, form_type, edit_item_id = None, edit_item_row = None):
    if request.method == 'POST':
        search_form = ITEM_SEARCH_FORMS[chosen_model_name](request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "date_interval" or search_column == "cost":
                interval_borders = [search_form.cleaned_data.get("interval_start"), search_form.cleaned_data.get("interval_end")]
                request_params[search_column] = ", ".join(interval_borders)
            else:
                request_params[search_column] = search_form.cleaned_data.get("common_text")
                if search_column == "unprocessed_applications":
                    request_params.pop("processed_applications", None)
                elif search_column == "processed_applications":
                    request_params.pop("unprocessed_applications", None)
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            if chosen_model_name == "Order":
                search_form = ChooseOrderSearchForm(form_data)
            else:
                search_form = ITEM_SEARCH_FORMS[chosen_model_name](form_data)
        else:
            if chosen_model_name == "Order":
                search_form = ChooseOrderSearchForm()
            else:
                search_form = ITEM_SEARCH_FORMS[chosen_model_name]()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params['url'] = request.path
    empty_table_phrase = "Список пуст"        
    chosen_model = MODELS[chosen_model_name].objects.all().order_by("id")
    if (chosen_model_name == "Order"):
        chosen_model = chosen_model.find_in_work()
    if request_params:
        chosen_model = chosen_model.find(request_params)
    if not chosen_model.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        chosen_model = chosen_model.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    context = {"search_form": search_form,
                "model_name": chosen_model_name,
                "title": CHOOSE_TABLE_NAME[chosen_model_name],
                "model": chosen_model, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": MODELS[chosen_model_name].get_fields_values_titles(), 
                "model_field_titles":MODELS[chosen_model_name].get_fields_titles_ru_en_dict(),
                "form_type": form_type,
                "form_model_name": form_model_name,
                "edit_item_id": edit_item_id,
                "edit_item_row": edit_item_row}
    return render(request, "choose-page.html", context)  


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Chief, login_url="log_reg:sign_in")
def confirm_order(request, item_id, row):
    object = get_object_or_404(Order, id=item_id)
    object.status = "Выполнен"
    object.save()
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url += "?" + urlencode(request_params) 
    previous_url += f"#table-row-{int(row) - 1}"
    return redirect(previous_url)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Chief, login_url="log_reg:sign_in")
def cancel_order_confirm(request, item_id, row):
    object = get_object_or_404(Order, id=item_id)
    object.status = "В работе"
    object.save()
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url += "?" + urlencode(request_params) 
    previous_url += f"#table-row-{int(row) - 1}"
    return redirect(previous_url)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(lambda user: is_Manager(user) or is_Chief(user), login_url="log_reg:sign_in")
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
                change_search_items_status(search_column, request_params)
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = ChiefOrderSearchForm(form_data) if (is_Chief(request.user) and not is_Superuser(request.user)) else OrderSearchForm(form_data)
        else:
            search_form = ChiefOrderSearchForm() if (is_Chief(request.user) and not is_Superuser(request.user)) else OrderSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"
    if is_Manager(request.user):        
        orders = Order.objects.all().order_by("id")
    elif is_Chief(request.user):
        orders = Order.objects.all().find_processed().order_by("id")
    if request_params:
        orders = orders.find(request_params)
    if not orders.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        orders = orders.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_Manager(request.user)
    context = {"search_form": search_form,
                "model_name": "Order",
                "title": "Журнал заказов",
                "model": orders, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Order.get_fields_values_titles(), 
                "model_field_titles":Order.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def clients_list(request):
    if request.method == 'POST':
        search_form = ClientSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = ClientSearchForm(form_data)
        else:
            search_form = ClientSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Каталог пуст"        
    clients = Client.objects.all().order_by("id")
    if request_params:
        clients = clients.find(request_params)
    if not clients.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        clients = clients.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_Manager(request.user)
    context = {"search_form": search_form,
                "model_name": "Client",
                "title": "Каталог клиентов",
                "model": clients, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Client.get_fields_values_titles(), 
                "model_field_titles":Client.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_PurchaseDepartmentEmployee, login_url="log_reg:sign_in")
def vendors_list(request):
    if request.method == 'POST':
        search_form = VendorSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = VendorSearchForm(form_data)
        else:
            search_form = VendorSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    vendors = Vendor.objects.all().order_by("id")
    if request_params:
        vendors = vendors.find(request_params)
    if not vendors.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        vendors = vendors.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_PurchaseDepartmentEmployee(request.user)
    context = {"search_form": search_form,
                "model_name": "Vendor",
                "title": "Каталог поставщиков",
                "model": vendors, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Vendor.get_fields_values_titles(), 
                "model_field_titles": Vendor.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_PurchaseDepartmentEmployee, login_url="log_reg:sign_in")
def materials_list(request):
    if request.method == 'POST':
        search_form = MaterialSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "cost":
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
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = MaterialSearchForm(form_data)
        else:
            search_form = MaterialSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    materials = Material.objects.all().order_by("id")
    if request_params:
        materials = materials.find(request_params)
    if not materials.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        materials = materials.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_PurchaseDepartmentEmployee(request.user)
    context = {"search_form": search_form,
                "model_name": "Material",
                "title": "Каталог материалов",
                "model": materials, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Material.get_fields_values_titles(), 
                "model_field_titles": Material.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Chief, login_url="log_reg:sign_in")
def employees_list(request):
    if request.method == 'POST':
        search_form = EmployeeSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = EmployeeSearchForm(form_data)
        else:
            search_form = EmployeeSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    employees = Employee.objects.all().order_by("id")
    if request_params:
        employees = employees.find(request_params)
    if not employees.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        employees = employees.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_Chief(request.user)
    context = {"search_form": search_form,
                "model_name": "Employee",
                "title": "Каталог сотрудников",
                "model": employees, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Employee.get_fields_values_titles(), 
                "model_field_titles": Employee.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Chief, login_url="log_reg:sign_in")
def machines_list(request):
    if request.method == 'POST':
        search_form = MachineSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = MachineSearchForm(form_data)
        else:
            search_form = MachineSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    machines = Machine.objects.all().order_by("id")
    if request_params:
        machines = machines.find(request_params)
    if not machines.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        machines = machines.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_Chief(request.user)
    context = {"search_form": search_form,
                "model_name": "Machine",
                "title": "Каталог станков",
                "model": machines, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Machine.get_fields_values_titles(), 
                "model_field_titles": Machine.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_PurchaseDepartmentEmployee, login_url="log_reg:sign_in")
def supplies_list(request):
    if request.method == 'POST':
        search_form = SupplySearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "date_interval" or search_column == "cost" or search_column == "quantity":
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
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = SupplySearchForm(form_data)
        else:
            search_form = SupplySearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    supplies = Supply.objects.all().order_by("id")
    print(supplies)
    if request_params:
        supplies = supplies.find(request_params)
    if not supplies.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        supplies = supplies.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_PurchaseDepartmentEmployee(request.user)
    context = {"search_form": search_form,
                "model_name": "Supply",
                "title": "Журнал поставок",
                "model": supplies, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Supply.get_fields_values_titles(), 
                "model_field_titles": Supply.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    for supply in supplies:
        print(supply.order.id)
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Chief, login_url="log_reg:sign_in")
def schedule(request):
    if request.method == 'POST':
        search_form = ScheduleSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "date_interval":
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
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = ScheduleSearchForm(form_data)
        else:
            search_form = ScheduleSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    supplies = Schedule.objects.all().order_by("id")
    if request_params:
        supplies = supplies.find(request_params)
    if not supplies.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    if sort_by_column is not None:
        supplies = supplies.sort(sort_by_column, sort_direction)
    if request_params:
        request_params ="?" + urlencode(request_params)
    is_allowed_to_modify = is_Chief(request.user)
    context = {"search_form": search_form,
                "model_name": "Schedule",
                "title": "График занятости",
                "model": supplies, 
                "empty_table_phrase" : empty_table_phrase, 
                "sort_direction": change_direction(sort_direction),
                "request_params": request_params, 
                "table_column_titles": Schedule.get_fields_values_titles(), 
                "model_field_titles": Schedule.get_fields_titles_ru_en_dict(),
                "is_Superuser": is_Superuser(request.user),
                "is_Manager": is_Manager(request.user),
                "is_Chief": is_Chief(request.user),
                "is_PurchaseDepartmentEmployee": is_PurchaseDepartmentEmployee(request.user),
                "is_allowed_to_modify": is_allowed_to_modify}
    return render(request, "table-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Manager, login_url="log_reg:sign_in")
def order_info(request, order_id, row):
    order = get_object_or_404(Order, id=order_id)
    supplies = Supply.objects.filter(order=order)
    tasks = Schedule.objects.filter(order=order)
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url += "?" + urlencode(request_params) 
    previous_url += f"#table-row-{int(row) - 1}"
    context = {
        "title": "Информация о заказе",
        "order": order,
        "supplies": supplies,
        "tasks": tasks,
        "previous_url": previous_url,
    }
    return render(request, "order-info.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_PurchaseDepartmentEmployee, login_url="log_reg:sign_in")
def monthly_spendings(request):
    if request.method == 'POST':
        search_form = MonthlySpendingsSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            if search_column == "month_interval" or search_column == "cost" or search_column == "total_cost":
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
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = MonthlySpendingsSearchForm(form_data)
        else:
            search_form = MonthlySpendingsSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    if sort_direction is not None:
        if sort_direction == "desc":
            sort_by_column = "-" + sort_by_column
    monthly_spendings = Supply.objects.annotate(period=TruncMonth("date")).values("period").annotate(total_cost=Sum('cost')).order_by("-period")
    if sort_by_column is not None:
        monthly_spendings = monthly_spendings.order_by(sort_by_column)
    # Ищем
    month_interval = request_params.get("month_interval")
    month = request_params.get("month")
    cost = request_params.get("total_cost")
    if month_interval is not None:
        interval_borders = month_interval.split(", ")
        start_interval = datetime.datetime.strptime(f"01.{interval_borders[0]}", "%d.%m.%Y")
        end_interval = datetime.datetime.strptime(f"01.{interval_borders[1]}", "%d.%m.%Y")
        monthly_spendings = monthly_spendings.filter(Q(period__gte=start_interval) & Q(period__lte=end_interval))
    if month is not None and month:
        month_period = datetime.datetime.strptime(f"01.{month}", "%d.%m.%Y")
        monthly_spendings = monthly_spendings.filter(period=month_period)
    if cost is not None and cost:
        interval_borders = cost.split(", ")
        monthly_spendings = monthly_spendings.filter(Q(total_cost__gte=int(interval_borders[0])) & Q(total_cost__lte=int(interval_borders[1])))
    formatted_monthly_spendings = []
    empty_table_phrase = "Список пуст"  
    if not monthly_spendings.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    for item in monthly_spendings: 
        period = item['period'].strftime("%B %Y")
        space_index = period.find(" ")
        period = MONTHS[period[:space_index]] + period[space_index: ]
        formatted_monthly_spendings.append({ 'period': period, 'total_cost': item['total_cost'] })
    request_params["url"] = request.path
    previous_url = reverse("employee:supplies") + "?" + urlencode(request_params)
    request_params = "?" + urlencode(request_params)
    context = {
        "search_form": search_form,
        "title": "Месячные расходы",
        "monthly_spendings": formatted_monthly_spendings,
        "previous_url": previous_url,
        "sort_direction": change_direction(sort_direction),
        "request_params": request_params,
        "empty_table_phrase": empty_table_phrase,
    }
    return render(request, "monthly-spendings.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Admin, login_url="log_reg:sign_in")
def users_list(request):
    if request.method == 'POST':
        search_form = UserSearchForm(request.POST)
        request_params = request.GET.copy()
        if search_form.is_valid():
            search_column = search_form.cleaned_data.get("search_column")
            request_params[search_column] = search_form.cleaned_data.get("common_text")
            return redirect(request.path + "?" + urlencode(request_params))
        else: 
            request.session['form_data'] = request.POST
            if request_params:
                return redirect(request.path + "?" + urlencode(request_params))
    else:
        form_data = request.session.pop('form_data', None)
        if form_data is not None:
            search_form = UserSearchForm(form_data)
        else:
            search_form = UserSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    users = User.objects.all().order_by("id")
    # Сортируем
    if sort_direction is not None:
        if sort_direction == "desc":
            sort_by_column = "-" + sort_by_column
    if sort_by_column is not None:
        if not sort_by_column.endswith("role"):
            users = users.order_by(sort_by_column)
    # Ищем
    username = request_params.get("username")
    role = request_params.get("role")
    if username is not None and username:
        users = users.filter(username__icontains=username)
    if role is not None and role:
        users = users.filter(groups__name=role)
    expanded_users = []
    for user in users:
        user_groups = user.groups.all()
        group_names = ", ".join([group.name for group in user_groups])
        expanded_users.append({"id": user.id, "username": user.username, "role": group_names, "is_Superuser": is_Superuser(user)})
    if sort_by_column is not None:
        if sort_by_column.endswith("role"):
            expanded_users = sorted(expanded_users, key=lambda user: user["role"], reverse=True if sort_by_column[0] == '-' else False)
    empty_table_phrase = "Список пуст"  
    if not users.exists():
        empty_table_phrase = "Нет записей, удовлетворяющих заданным условиям."
    request_params["url"] = request.path
    previous_url = reverse("employee:supplies") + "?" + urlencode(request_params)
    request_params = "?" + urlencode(request_params)
    context = {
        "search_form": search_form,
        "title": "Список пользователей",
        "users": expanded_users,
        "previous_url": previous_url,
        "sort_direction": change_direction(sort_direction),
        "request_params": request_params,
        "empty_table_phrase": empty_table_phrase,
        "is_Superuser": is_Superuser(request.user)
    }
    return render(request, "users-list.html", context)