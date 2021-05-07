from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.gis.db.models import MultiPointField
from django.db import models

from django_countries.fields import CountryField
from app.core.validators import PhoneNumberValidator

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
    phone_number = models.CharField(max_length=16, unique=True, validators=(PhoneNumberValidator,))
    country = CountryField()
    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    CLIENT_ROLE = 1
    EMPLOYEE_ROLE = 2
    ROLE_TYPES = (
        (CLIENT_ROLE, 'Client'),
        (EMPLOYEE_ROLE, 'Employee')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_TYPES)
    # Client
    passport = models.CharField(max_length=9, unique=True)
    # Employee

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class CargoFeature(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CarType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Car(models.Model):
    number = models.CharField(max_length=10)
    country = CountryField()
    type = models.ForeignKey('core.CarType', on_delete=models.CASCADE, related_name='cars')
    brand = models.ForeignKey('core.CarBrand', on_delete=models.CASCADE, related_name='cars')
    lifting = models.PositiveSmallIntegerField()


class CountryCoordinates(models.Model):
    iso = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Order(models.Model):
    CREATED_TYPE = 1
    ACCEPTED_TYPE = 2
    FINISHED_TYPE = 3
    STATUS_TYPES = (
        (CREATED_TYPE, 'Created'),
        (ACCEPTED_TYPE, 'Accepted'),
        (FINISHED_TYPE, 'Finished')
    )
    status = models.PositiveSmallIntegerField(default=CREATED_TYPE, choices=STATUS_TYPES)
    from_to_points = MultiPointField()
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

    def accept(self):
        self.accept_datetime = datetime.now()
        self.status = Order.ACCEPTED_TYPE

    def finish(self):
        self.finish_datetime = datetime.now()
        self.status = Order.FINISHED_TYPE
