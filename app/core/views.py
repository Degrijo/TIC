import asyncio
from datetime import datetime

import schedule
from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView

from app.core.forms import SignUpClientForm, SignUpEmployeeForm, LogInForm, CreateOrderForm
from app.core.mixins import EmployeeMixin, ClientMixin, ParticipantMixin

# Главная страница, Регистрация Клиента (имя, фамилия, пароль, паспорт, страна, номер телефона, почта),
# Вход Клиента (номер телефона/почта, пароль), Регистрация работника (имя, фамилия, пароль, номер телефона, страна
# почта), Вход работника (номер телефона/почта, пароль), # Личный кабинет (имя, фамилия, страна,
# заказы с деталями),
# Оформление заказа для Клиента (типы грузов, масса, начальная и конечная точки), Список прошлых заказов Клиента
# (откуда, куда, ссылка на детали, время начала и конца), Список актуальных заказов для Работника, Детали заказа (отслеживание)
from app.core.models import Car, Order


class MainPageView(TemplateView):
    template_name = 'core/main_page.html'
    extra_context = {'title': 'Main page', 'user_model': get_user_model()}


class SignUpClientView(FormView):
    template_name = 'core/signup_client.html'
    form_class = SignUpClientForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up: client', 'user_model': get_user_model()}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInView(FormView):
    template_name = 'core/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Login', 'user_model': get_user_model()}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignUpEmployeeView(FormView):
    template_name = 'core/signup_employee.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up: employee', 'user_model': get_user_model()}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('main_page')


class CreateOrderView(ClientMixin, FormView):
    template_name = 'core/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('list_my_orders')
    extra_context = {'title': 'Create order', 'user_model': get_user_model()}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        coors = self.request.user.country_coordinates
        form.fields['from_to_points'].widget.attrs['default_lat'] = coors[0]
        form.fields['from_to_points'].widget.attrs['default_lon'] = coors[1]
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class ListMyOrdersView(ListView):
    template_name = 'core/list_my_orders.html'
    extra_context = {'title': 'List my orders', 'order_model': Order, 'user_model': get_user_model()}
    ordering = '-start_datetime'

    def get_queryset(self):
        user = self.request.user
        if user.role == get_user_model().CLIENT_ROLE:
            return Order.objects.filter(sender=user)
        elif user.role == get_user_model().EMPLOYEE_ROLE:
            return Order.objects.filter(employee=user)


class ListActualOrdersView(EmployeeMixin, ListView):
    template_name = 'core/list_actual_orders.html'
    queryset = Order.objects.filter(status=Order.CREATED_TYPE)
    success_url = reverse_lazy('list_my_orders')
    extra_context = {'title': 'List actual orders', 'user_model': get_user_model()}
    ordering = '-start_datetime'


async def accept_order(order_id):
    await asyncio.sleep(30)
    Order.objects.get(id=order_id).finish()


class AcceptOrderView(EmployeeMixin, UpdateView):
    success_url = reverse_lazy('list_my_orders')
    queryset = Order.objects.filter(status=Order.CREATED_TYPE)
    extra_context = {'title': 'Accept order'}
    fields = ('car',)
    template_name = 'core/accept_order.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.employee = self.request.user
        self.object.accept_datetime = datetime.now()
        self.object.status = Order.ACCEPTED_TYPE
        self.object.save()
        form.save_m2m()
        asyncio.run(accept_order(self.object.id))
        return HttpResponseRedirect(self.get_success_url())


class DetailOrderView(ParticipantMixin, DetailView):
    model = Order
    template_name = 'core/detail_order.html'
    extra_context = {'title': 'Order details', 'user_model': get_user_model()}

    def get_success_url(self):
        success_url = reverse_lazy('detail_order', pk=self.kwargs['pk'])
        return str(success_url)

    def post(self):
        object = self.get_object()
        object.finish()
        return HttpResponseRedirect(self.get_success_url())


class CreateCarView(EmployeeMixin, CreateView):
    template_name = 'core/create_car.html'
    model = Car
    fields = '__all__'
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Create Car', 'user_model': get_user_model()}
