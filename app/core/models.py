from django.contrib.auth.models import AbstractUser
from django.db import models

# 3) пользователь выбирает работника, заказывает перевозку, работник забирает груз и доставляет
# Клиент, Работник(автомобили), Свойство Груза(стекло, одежда, еда, мебель, строительные материалы, техника),
# Автомобиль (номер, тип, грузоподъемность), Тип Авто (газель, фура)
# Перевозка(откуда, куда, цена, время принятия заказы, время завершения заказа, груз, клиент1, клиент2, работник, автомобиль, масса и свойста груза)


class Client(AbstractUser):
    # common
    phone_number = models.CharField(max_length=12)  # добавлять + в начало
    country = models.CharField()
    CLIENT_ROLE = 1
    EMPLOYEE_ROLE = 2
    ROLE_TYPE = (
        (CLIENT_ROLE, 'Client'),
        (EMPLOYEE_ROLE, 'Employee')
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_TYPE)
    # Client
    passport = models.CharField(max_length=9)
    # Employee


class CargoFeature(models.Model):
    name = models.CharField(max_length=256)
