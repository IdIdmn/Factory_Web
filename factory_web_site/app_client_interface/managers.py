from django.db import models
from django.db.models import Q
import datetime

class OrderQuerySet(models.QuerySet): 

    def find_by_date_interval(self, start_interval_date, end_interval_date):
        return self.filter(Q(date__gte=start_interval_date) & Q(date__lte=end_interval_date))
    
    def find_by_order_type(self, order_type, include=False):
        if include:
            return self.filter(order_type__icontains=order_type.lower())
        else:
            return self.filter(order_type=order_type.capitalize())
        
    def find_by_date(self, date):
        return self.filter(date=date)
    
    def find_by_cost_interval(self, start_interval_cost, end_interval_cost):
        return self.filter(Q(cost__gte=start_interval_cost) & Q(cost__lte=end_interval_cost))
    
    def find_by_client_email(self, email, include=False):
        if include:
            return self.filter(client__email__icontains=email)
        else:
            return self.filter(client__email=email)

    def find_unprocessed(self):
        return self.filter(status="На рассмотрении")

    def find_processed(self):
        return self.exclude(status="На рассмотрении")

    def find_in_work(self):
        return self.filter(status="В работе")
    
    def find_executed(self):
        return self.filter(status="Выполнен")

    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)
        
    def find(self, request_params):
        unprocessed = request_params.get("unprocessed_applications", None)
        processed = request_params.get("processed_applications", None)
        in_work = request_params.get("in_work", None)
        executed = request_params.get("executed", None)
        order_type = request_params.get("order_type", None)
        date = request_params.get("date", None)
        date_interval_borders = request_params.get("date_interval", None)
        cost_interval_borders = request_params.get("cost", None)
        email = request_params.get("email", None)
        if email is not None and email:
            self = self.find_by_client_email(email, include=True)
        if date_interval_borders is not None:
            date_interval_borders = date_interval_borders.split(", ")
            self = self.find_by_date_interval(datetime.datetime.strptime(date_interval_borders[0], "%d.%m.%Y"), datetime.datetime.strptime(date_interval_borders[1], "%d.%m.%Y"))
        if order_type is not None and order_type:
            self = self.find_by_order_type(order_type, include = True)
        if date is not None and date:
            self = self.find_by_date(datetime.datetime.strptime(date, "%d.%m.%Y"))
        if cost_interval_borders is not None:
            cost_interval_borders = cost_interval_borders.split(", ")
            self = self.find_by_cost_interval(int(cost_interval_borders[0]), int(cost_interval_borders[1]))
        if unprocessed is not None:
            self = self.find_unprocessed()
        if processed is not None:
            self = self.find_processed()
        if in_work is not None:
            self = self.find_in_work()
        if executed is not None:
            self = self.find_executed()
        return self


class OrderManager(models.Manager):

    def get_queryset(self): 
        return OrderQuerySet(self.model, using=self._db)
    

class ClientQuerySet(models.QuerySet): 

    def find_by_email(self, email, include=False):
        if include:
            return self.filter(email__icontains=email)
        else:
            return self.filter(email=email)
    
    def find_by_full_name(self, name, include=False):
        if include:
            return self.filter(full_name__icontains=name.lower())
        else:
            return self.filter(full_name=name.capitalize())
        
    def find_by_phone_number(self, phone_number):
        print(phone_number)
        return self.filter(phone_number=phone_number)
        
    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        email = request_params.get("email", None)
        full_name = request_params.get("full_name", None)
        phone_number = request_params.get("phone_number", None)
        if email is not None and email:
            self = self.find_by_email(email, include=True)
        if full_name is not None and full_name:
            self = self.find_by_full_name(full_name, include=True)
        if phone_number is not None and phone_number:
            self = self.find_by_phone_number(phone_number)
        return self


class ClientManager(models.Manager):

    def get_queryset(self): 
        return ClientQuerySet(self.model, using=self._db)
