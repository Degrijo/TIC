from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.gis.db.models import MultiPointField
from django.db import models
from django.utils import timezone

from django_countries.fields import CountryField

from app.core.utils import order_mailing
from app.core.validators import PhoneNumberValidator
from config.settings.common import DATETIME_FORMAT


class UserManager(BaseUserManager):
    def create_client(self, first_name, last_name, email, passport, country, phone_number, password1):
        user = self.model(first_name=first_name, last_name=last_name, email=email.lower(), passport=passport,
                          country=country, phone_number=phone_number, role=self.model.CLIENT_ROLE)
        user.set_password(password1)
        user.save()
        return user

    def create_employee(self, first_name, last_name, email, passport, country, phone_number, password1):
        user = self.model(first_name=first_name, last_name=last_name, email=email.lower(), passport=passport,
                          country=country, phone_number=phone_number, role=self.model.EMPLOYEE_ROLE)
        user.set_password(password1)
        user.save()
        return user


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

    @property
    def country_coordinates(self):
        coors = CountryCoordinates.objects.get(iso=self.country.code)
        return coors.latitude, coors.longitude


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

    def __str__(self):
        return f'{self.brand} {self.type} {self.number}'


class CountryCoordinates(models.Model):
    iso = models.CharField(max_length=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Order(models.Model):
    CREATED_TYPE = 1
    ACCEPTED_TYPE = 2
    FINISHED_TYPE = 3
    STATUS_COLORS = (
        (CREATED_TYPE, '#0022FF'),
        (ACCEPTED_TYPE, '#FFFF00'),
        (FINISHED_TYPE, '#11FF00')
    )
    STATUS_TYPES = (
        (CREATED_TYPE, 'Created'),
        (ACCEPTED_TYPE, 'Accepted'),
        (FINISHED_TYPE, 'Finished')
    )
    status = models.PositiveSmallIntegerField(default=CREATED_TYPE)
    from_to_points = MultiPointField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    start_datetime = models.DateTimeField(default=timezone.now)
    accept_datetime = models.DateTimeField(blank=True, null=True)
    finish_datetime = models.DateTimeField(blank=True, null=True)
    mass = models.PositiveSmallIntegerField()
    cargo_features = models.ManyToManyField('core.CargoFeature', related_name='orders')
    sender = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='packages')
    recipient = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='parcels')
    employee = models.ForeignKey('core.CustomUser', on_delete=models.CASCADE, related_name='orders', blank=True, null=True)
    car = models.ForeignKey('core.Car', on_delete=models.CASCADE, related_name='orders', blank=True, null=True)

    def __str__(self):
        string = f'{self.start_datetime.strftime(DATETIME_FORMAT)}'
        if self.accept_datetime:
            string += ' -> ' + self.accept_datetime.strftime(DATETIME_FORMAT)
        if self.finish_datetime:
            string += ' -> ' + self.finish_datetime.strftime(DATETIME_FORMAT)
        string += f' - {self.price} BYN'
        return string

    @property
    def color(self):
        return dict(Order.STATUS_COLORS).get(self.status)

    @property
    def types(self):
        final = []
        types = dict(Order.STATUS_TYPES)
        for number, color in Order.STATUS_COLORS:
            final.append((color, types[number]))
        return final

    def accept(self, employee):
        self.employee = employee
        self.accept_datetime = timezone.now()
        self.status = Order.ACCEPTED_TYPE
        self.save(update_fields=('status', 'employee', 'accept_datetime'))
        # context = {'order': self,
        #            'user_model': get_user_model()}
        # order_mailing(self, 'emails/accept_email.html', context, 'order accepted')

    def finish(self):
        self.finish_datetime = timezone.now()
        self.status = Order.FINISHED_TYPE
        self.save(update_fields=('status', 'finish_datetime'))
        # context = {'order': self,
        #            'user_model': get_user_model()}
        # order_mailing(self, 'emails/accept_email.html', context, 'order accepted')
