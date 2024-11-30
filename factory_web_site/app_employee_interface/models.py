from django.db import models
from django.forms import DateField
from app_client_interface.models import Order
from .managers import *

class Vendor(models.Model):
    company_name = models.CharField()
    email = models.CharField()

    objects = VendorManager()

    class Meta:
        ordering = ["company_name"]

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "Название компании": "company_name" , "Почтовый адрес поставщика": "email"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID", "Название компании", "Почтовый адрес поставщика"]
    
    @property
    def fields_values(self):
        return [self.id, self.company_name, self.email]


class Material(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="materials", on_delete=models.CASCADE)
    metal_type = models.CharField()
    metal_grade = models.CharField()
    cost = models.FloatField()

    objects = MaterialManager()

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "Поставщик": "vendor" , "Тип металла": "metal_type", "Марка металла": "metal_grade", "Цена за ед., руб." : "cost"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID", "Поставщик", "Тип металла", "Марка металла", "Цена за ед., руб."]
    
    @property
    def fields_values(self):
        return [self.id, self.vendor.company_name, self.metal_type, self.metal_grade, self.cost]


class Employee(models.Model):
    full_name = models.CharField()
    specialty = models.CharField()
    salary = models.IntegerField(null=True)

    objects = EmployeeManager()

    class Meta:
        ordering = ["full_name"]

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "ФИО": "full_name" , "Специальность": "specialty", "Зарплата, руб/час": "salary"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID", "ФИО", "Специальность", "Зарплата, руб/час"]
    
    @property
    def fields_values(self):
        return [self.id, self.full_name, self.specialty, self.salary]


class Machine(models.Model):
    serial_number = models.CharField()
    machine_name = models.CharField()
    specialty = models.CharField()

    objects = MachineManager()

    class Meta:
        ordering = ["serial_number"]

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID": "id", "Серийный номер": "serial_number" , "Название": "machine_name", "Специальность": "specialty"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID", "Серийный номер", "Название", "Специальность"]
    
    @property
    def fields_values(self):
        return [self.id, self.serial_number ,self.machine_name, self.specialty]


class Supply(models.Model):
    order = models.ForeignKey(Order, related_name="supplies", on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Material, related_name="supplies", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    cost = models.FloatField()

    objects = SupplyManager()

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID заказа": "order", "ID материала": "material" , "Дата": "date", "Количество": "quantity", "Стоимость": "cost"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID заказа", "ID материала" , "Дата", "Количество", "Стоимость"]
    
    @property
    def fields_values(self):
        return [self.order.id, self.material.id ,self.date, self.quantity, self.cost]



class Schedule(models.Model):
    order = models.ForeignKey(Order, related_name="tasks", on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, related_name="tasks", on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, related_name="tasks", on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    objects = ScheduleManager()

    @staticmethod
    def get_fields_titles_ru_en_dict():
        return {"ID заказа": "order", "ID сотрудника": "employee" , "ID станка": "machine", "Дата начала работ": "start_date", "Дата окончания работ": "end_date"}
    
    @staticmethod
    def get_fields_values_titles():
        return ["ID заказа", "ID сотрудника" , "ID станка", "Дата начала работ", "Дата окончания работ"]
    
    @property
    def fields_values(self):
        return [self.order.id, self.employee.id ,self.machine.id, self.start_date, self.end_date]