from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import model_to_dict
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required


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
    user_orders = request.user.client_info.orders.all()
    return render(request, "client-profile.html", {'title': "Профиль", "user_orders": user_orders, "order_field_titles": Order.get_profile_order_list_titles()})

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
