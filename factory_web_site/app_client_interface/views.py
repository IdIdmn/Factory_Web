from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import OrderForm


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
            form = OrderForm(form_data, filename = file_name)
        else:
            form = OrderForm()
    return render(request, "MainPage.html", {'form': form, 'title': "МОЗ №1"})

