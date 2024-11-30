from urllib.parse import urlencode
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from app_client_interface.models import Order
from .forms import *
from django.shortcuts import get_object_or_404

ITEM_EDIT_FORMS = {"Order": OrderEditForm, "Client": ClientEditForm, "Vendor": VendorEditForm, "Material": MaterialEditForm, "Employee": EmployeeEditForm,
                        "Machine": MachineEditForm, "Supply": SupplyEditForm, "Schedule": ScheduleEditForm}

ITEM_CREATE_FORMS = {"Order": OrderCreateForm, "Vendor": VendorCreateForm, "Material": MaterialCreateForm,  "Employee": EmployeeCreateForm, "Machine": MachineCreateForm,
                        "Supply": SupplyCreateForm, "Schedule": ScheduleCreateForm}

MODELS = {"Order": Order, "Client": Client, "Vendor": Vendor, "Material":Material, "Employee": Employee, "Machine": Machine, "Supply": Supply, "Schedule": Schedule}

OBJECT_TYPES = {"Order": "о заказе", "Client": "о клиенте", "Vendor": "о поставщике", "Material": "о материале" , "Employee": "о сотруднике", "Machine": "о станке",
                    "Supply": "о поставке", "Schedule": "записи в графике занятости"}


def is_Manager(user):
    return user.groups.filter(name='Manager').exists()


def is_PurchaseDepartmentEmployee(user):
    return user.groups.filter(name='PurchaseDepartment').exists()


def is_Chief(user):
    return user.groups.filter(name='Chief').exists()


def is_Employee(user):
    return is_Manager(user) or is_PurchaseDepartmentEmployee(user) or is_Chief(user)


def is_Superuser(user):
    return is_Manager(user) and is_PurchaseDepartmentEmployee(user) and is_Chief(user)


def change_direction(sort_direction):
    if sort_direction == "desc" or sort_direction is None:
        return "asc"
    else:
        return "desc"


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def sort_table(request, model, sort_by_column, sort_direction):
    if sort_direction == "desc" and request.session.pop('previous_sorted_model', None) != f"{model}-{sort_by_column}":
        sort_direction = "asc"
    request.session['sort_direction'] = sort_direction
    request.session['sort_by_column'] = sort_by_column
    request.session['previous_sorted_model'] = f"{model}-{sort_by_column}"
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
    return redirect(request_params.pop("url")[0])


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def delete_item(request, model_name, item_id, row):
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
def create_item(request, model_name):
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url = previous_url + "?" + urlencode(request_params)
    if request.method == "POST":
        form = ITEM_CREATE_FORMS[model_name](request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(previous_url)
    else:
        form = ITEM_CREATE_FORMS[model_name]()
    context = {"form": form, "title": "Редактирование", "previous_url" : previous_url, "object_type": OBJECT_TYPES[model_name]}
    return render(request, "add-edit-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
def edit_item(request, model_name, item_id, row):
    request_params = request.GET.copy()
    previous_url = request_params.pop("url")[0]
    if request_params:
        previous_url += "?" + urlencode(request_params) 
    previous_url += f"#table-row-{int(row) - 1}"
    if request.method == "POST":
        form = ITEM_EDIT_FORMS[model_name](request.POST, id = item_id)
        if form.is_valid():
            form.save()
            return redirect(previous_url)
    else:
        item = get_object_or_404(MODELS[model_name], id=item_id)
        form = ITEM_EDIT_FORMS[model_name](initial=model_to_dict(item), id = item_id)
    context = {
        "form": form,
        "title": "Редактирование", 
        "previous_url" : previous_url, 
        "object_type": OBJECT_TYPES[model_name]
    }
    return render(request, "add-edit-page.html", context)


@login_required(login_url="log_reg:sign_in")
@user_passes_test(is_Employee, login_url="log_reg:sign_in")
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
            search_form = OrderSearchForm(form_data)
        else:
            search_form = OrderSearchForm()
    sort_direction = request.session.pop('sort_direction', None)
    sort_by_column = request.session.pop('sort_by_column', None)
    request_params = request.GET.copy()
    request_params["url"] = request.path
    empty_table_phrase = "Список пуст"        
    orders = Order.objects.all().order_by("id")
    if request_params:
        orders = orders.find(request_params)
    if orders.count() == 0:
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
    if clients.count() == 0:
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
    if vendors.count() == 0:
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
    if materials.count() == 0:
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
    if employees.count() == 0:
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
    if machines.count() == 0:
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
    if request_params:
        supplies = supplies.find(request_params)
    if supplies.count() == 0:
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
    if supplies.count() == 0:
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

