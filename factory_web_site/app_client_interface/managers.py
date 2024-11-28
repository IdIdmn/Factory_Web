from django.db import models
from django.db.models import Sum, Q
from django.db.models.functions import Lower

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

    def sort_orders(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)
        

class OrderManager(models.Manager):

    def get_queryset(self): 
        return OrderQuerySet(self.model, using=self._db)
