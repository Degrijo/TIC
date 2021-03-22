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


# Автомобиль
class Car(models.Model):
    car_number = models.PositiveSmallIntegerField() #номер автомобиля
    type = models.CharField(max_length=30) # тип мерс или порше
    lifting = models.PostitiveIntegerField() # грузоподьемность
    car_type = models.CharField('gazel', 'fura') #тип газель или фура или легковушка

# Рейтинг Автомобиля или же водителя???
class Rating(models.Model):
    star = models.ForeignKey(Car,on_delete=models.CASCADE, verbose_name='zvezda')
    car_type = models.ForeignKey(Car,on_delete=models.CharField, verbose_name='gazel ili fura')

    def __str__(self):
        return f"{self.star} - {self.car_type}"


# Отзывы
class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('imya', max_length=100)
    text = models.TextField('soobshenie', max_length=5000)
    parent =models.ForeignKey('self', verbose_name = 'roditel',on_delete=models.SET_NULL, blank=True, null=True)
    car_type = models.ForeignKey(Car,verbose_name='gazel ili fura',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.car_type}"

