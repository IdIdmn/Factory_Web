from django.db import models
from django.db.models import Q
import datetime


# ----------------------- Поставщики -----------------------

class VendorQuerySet(models.QuerySet): 

    def find_by_email(self, email, include=False):
        if include:
            return self.filter(email__icontains=email)
        else:
            return self.filter(email=email)
    
    def find_by_name(self, company_name, include=False):
        if include:
            return self.filter(company_name__icontains=company_name)
        else:
            return self.filter(company_name=company_name)

    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        email = request_params.get("email", None)
        company_name = request_params.get("company_name", None)
        if email is not None and email:
            self = self.find_by_email(email, include=True)
        if company_name is not None and company_name:
            self = self.find_by_name(company_name, include=True)
        return self


class VendorManager(models.Manager):

    def get_queryset(self): 
        return VendorQuerySet(self.model, using=self._db)
    

# ----------------------- Материалы -----------------------

class MaterialQuerySet(models.QuerySet): 

    def find_by_company_name(self, company_name, include=False):
        if include:
            return self.filter(vendor__company_name__icontains=company_name)
        else:
            return self.filter(vendor__company_name=company_name)
    
    def find_by_metal_type(self, metal_type, include=False):
        if include:
            return self.filter(metal_type__icontains=metal_type)
        else:
            return self.filter(metal_type=metal_type)
        
    def find_by_metal_grade(self, metal_grade, include=False):
        if include:
            return self.filter(metal_grade__icontains=metal_grade)
        else:
            return self.filter(metal_grade=metal_grade)
    
    def find_by_cost_interval(self, start_interval_cost, end_interval_cost):
        return self.filter(Q(cost__gte=start_interval_cost) & Q(cost__lte=end_interval_cost))
    
    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        company_name = request_params.get("vendor", None)
        metal_type = request_params.get("metal_type", None)
        metal_grade = request_params.get("metal_grade", None)
        cost_interval_borders = request_params.get("cost", None)
        if company_name is not None and company_name:
            self = self.find_by_company_name(company_name, include=True)
        if metal_type is not None and metal_type:
            self = self.find_by_metal_type(metal_type, include=True)
        if metal_grade is not None and metal_grade:
            self = self.find_by_metal_grade(metal_grade, include=True)
        if cost_interval_borders is not None:
            cost_interval_borders = cost_interval_borders.split(", ")
            self = self.find_by_cost_interval(int(cost_interval_borders[0]), int(cost_interval_borders[1]))
        return self


class MaterialManager(models.Manager):

    def get_queryset(self): 
        return MaterialQuerySet(self.model, using=self._db)
    

# ----------------------- Сотрудники -----------------------

class EmployeeQuerySet(models.QuerySet): 

    def find_by_full_name(self, full_name, include=False):
        if include:
            return self.filter(full_name__icontains=full_name)
        else:
            return self.filter(full_name=full_name)
    
    def find_by_specialty(self, specialty, include=False):
        if include:
            return self.filter(specialty__icontains=specialty)
        else:
            return self.filter(specialty=specialty)

    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        full_name = request_params.get("full_name", None)
        specialty = request_params.get("specialty", None)
        if full_name is not None and full_name:
            self = self.find_by_full_name(full_name, include=True)
        if specialty is not None and specialty:
            self = self.find_by_specialty(specialty, include=True)
        return self


class EmployeeManager(models.Manager):

    def get_queryset(self): 
        return EmployeeQuerySet(self.model, using=self._db)

# ----------------------- Станки -----------------------

class MachineQuerySet(models.QuerySet): 

    def find_by_serial_number(self, serial_number, include=False):
        if include:
            return self.filter(serial_number__icontains=serial_number)
        else:
            return self.filter(serial_number=serial_number)
    
    def find_by_machine_name(self, machine_name, include=False):
        if include:
            return self.filter(machine_name__icontains=machine_name)
        else:
            return self.filter(machine_name=machine_name)
    
    def find_by_specialty(self, specialty, include=False):
        if include:
            return self.filter(specialty__icontains=specialty)
        else:
            return self.filter(specialty=specialty)

    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        serial_number = request_params.get("serial_number", None)
        machine_name = request_params.get("machine_name", None)
        specialty = request_params.get("specialty", None)
        if serial_number is not None and serial_number:
            self = self.find_by_serial_number(serial_number, include=True)
        if machine_name is not None and machine_name:
            self = self.find_by_machine_name(machine_name, include=True)
        if specialty is not None and specialty:
            self = self.find_by_specialty(specialty, include=True)
        return self


class MachineManager(models.Manager):

    def get_queryset(self): 
        return MachineQuerySet(self.model, using=self._db)
    
# ----------------------- Станки -----------------------

class SupplyQuerySet(models.QuerySet): 

    def find_by_order(self, order_id):
        return self.filter(order__id=order_id)
    
    def find_by_material(self, material_id, include=False):
        return self.filter(material__id=material_id)
    
    def find_by_date_interval(self, start_interval_date, end_interval_date):
        return self.filter(Q(date__gte=start_interval_date) & Q(date__lte=end_interval_date))
    
    def find_by_date(self, date):
        return self.filter(date=date)
    
    def find_by_quantity_interval(self, start_interval_quantity, end_interval_quantity):
        return self.filter(Q(quantity__gte=start_interval_quantity) & Q(quantity__lte=end_interval_quantity))
    
    def find_by_cost_interval(self, start_interval_cost, end_interval_cost):
        return self.filter(Q(cost__gte=start_interval_cost) & Q(cost__lte=end_interval_cost))

    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        date = request_params.get("date", None)
        date_interval_borders = request_params.get("date_interval", None)
        cost_interval_borders = request_params.get("cost", None)
        quantity_interval_borders = request_params.get("quantity", None)
        order_id = request_params.get("order_id", None)
        material_id = request_params.get("material_id", None)
        if order_id is not None and order_id:
            self = self.find_by_order(order_id)
        if material_id is not None and material_id:
            self = self.find_by_material(material_id)
        if date_interval_borders is not None:
            date_interval_borders = date_interval_borders.split(", ")
            self = self.find_by_date_interval(datetime.datetime.strptime(date_interval_borders[0], "%d.%m.%Y"), datetime.datetime.strptime(date_interval_borders[1], "%d.%m.%Y"))
        if date is not None and date:
            self = self.find_by_date(datetime.datetime.strptime(date, "%d.%m.%Y"))
        if cost_interval_borders is not None:
            cost_interval_borders = cost_interval_borders.split(", ")
            self = self.find_by_cost_interval(int(cost_interval_borders[0]), int(cost_interval_borders[1]))
        if quantity_interval_borders is not None:
            quantity_interval_borders = quantity_interval_borders.split(", ")
            self = self.find_by_quantity_interval(quantity_interval_borders[0], quantity_interval_borders[1])
        return self


class SupplyManager(models.Manager):

    def get_queryset(self): 
        return SupplyQuerySet(self.model, using=self._db)
    

# ----------------------- График занятости -----------------------


class ScheduleQuerySet(models.QuerySet): 

    def find_by_order(self, order_id):
        return self.filter(order__id=order_id)
    
    def find_by_employee(self, employee_id):
        return self.filter(employee__id=employee_id)
    
    def find_by_machine(self, machine_id):
        return self.filter(machine__id=machine_id)
    
    def find_by_start_date(self, start_date):
        return self.filter(start_date=start_date)
    
    def find_by_end_date(self, end_date):
        return self.filter(end_date=end_date)

    def find_by_date_interval(self, start_interval_date, end_interval_date):
        return self.filter(Q(start_date__gte=start_interval_date) & Q(end_date__lte=end_interval_date))
    
    def sort(self, column, direction):
        if direction == "desc":
            column = "-" + column
        return self.order_by(column)

    def find(self, request_params):
        order_id = request_params.get("order_id", None)
        employee_id = request_params.get("employee_id", None)
        machine_id = request_params.get("machine_id", None)
        start_date = request_params.get("start_date", None)
        end_date = request_params.get("end_date", None)
        date_interval_borders = request_params.get("date_interval", None)
        if order_id is not None and order_id:
            self = self.find_by_order(order_id)
        if employee_id is not None and employee_id:
            self = self.find_by_employee(employee_id)
        if machine_id is not None and machine_id:
            self = self.find_by_machine(machine_id)
        if start_date is not None and start_date:
            self = self.find_by_start_date(datetime.datetime.strptime(start_date, "%d.%m.%Y"))
        if end_date is not None and end_date:
            self = self.find_by_end_date(datetime.datetime.strptime(end_date, "%d.%m.%Y"))
        if date_interval_borders is not None:
            date_interval_borders = date_interval_borders.split(", ")
            self = self.find_by_date_interval(datetime.datetime.strptime(date_interval_borders[0], "%d.%m.%Y"), datetime.datetime.strptime(date_interval_borders[1], "%d.%m.%Y"))
        return self


class ScheduleManager(models.Manager):

    def get_queryset(self): 
        return ScheduleQuerySet(self.model, using=self._db)
