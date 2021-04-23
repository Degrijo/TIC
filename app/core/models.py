from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.gis.db.models import PointField

from django_countries.fields import CountryField

# 3) пользователь выбирает работника, заказывает перевозку, работник забирает груз и доставляет
# Клиент, Работник(автомобили), Свойство Груза(стекло, одежда, еда, мебель, строительные материалы, техника),
# Автомобиль (номер, тип, грузоподъемность), Тип Авто (газель, фура)
# Перевозка(откуда, куда, цена, время принятия заказы, время завершения заказа, груз, клиент1, клиент2, работник, автомобиль, масса и свойста груза)


class UserManager(BaseUserManager):
    def create_client(self, first_name, last_name, email, passport, country, phone_number, password1):
        user = self.model(first_name=first_name, last_name=last_name, email=email.lower(), passport=passport,
                          country=country, phone_number=phone_number[1:], role=self.model.CLIENT_ROLE)
        user.set_password(password1)
        user.save()
        return user

    def create_employee(self, first_name, last_name, email, passport, country, phone_number, password1):
        user = self.model(first_name=first_name, last_name=last_name, email=email.lower(), passport=passport,
                          country=country, phone_number=phone_number[1:], role=self.model.EMPLOYEE_ROLE)
        user.set_password(password1)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_client()


class CustomUser(AbstractUser):
    # common
    phone_number = models.CharField(max_length=12, unique=True)
    country = CountryField()
    username = None
    email = models.EmailField(unique=True)
    CLIENT_ROLE = 1
    EMPLOYEE_ROLE = 2
    ROLE_TYPE = (
        (CLIENT_ROLE, 'Client'),
        (EMPLOYEE_ROLE, 'Employee')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_TYPE)
    # Client
    passport = models.CharField(max_length=9, unique=True)
    # Employee

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class CargoFeature(models.Model):
    name = models.CharField(max_length=256)


class CarBrand(models.Model):
    name = models.CharField(max_length=64)


class CarType(models.Model):
    name = models.CharField(max_length=64)


class Car(models.Model):
    number = models.CharField(max_length=10)
    country = CountryField()
    type = models.ForeignKey('core.CarType', on_delete=models.CASCADE, related_name='cars')
    brand = models.ForeignKey('core.CarBrand', on_delete=models.CASCADE, related_name='cars')
    lifting = models.PositiveSmallIntegerField()


class Order(models.Model):
    start_point = PointField()
    end_point = PointField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    start_datetime = models.DateTimeField(auto_now_add=True)
    accept_datetime = models.DateTimeField(blank=True, null=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)
    mass = models.PositiveSmallIntegerField()
    cargo_features = models.ManyToManyField('core.CargoFeature', related_name='orders')
    sender = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='packages')
    recipient = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='parcels')
    employee = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    car = models.ForeignKey('core.Car', on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
