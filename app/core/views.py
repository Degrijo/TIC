from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView, ListView
from django.views.generic.detail import SingleObjectMixin, DetailView

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
    extra_context = {'title': 'Главная страница'}


class SignUpClientView(FormView):
    template_name = 'core/signup_client.html'
    form_class = SignUpClientForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Регистрация: клиент'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInView(FormView):
    template_name = 'core/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Вход'}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignUpEmployeeView(FormView):
    template_name = 'core/signup_employee.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Регистрация: сотрудник'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('main_page')


class CreateOrderView(ClientMixin, FormView):
    template_name = 'core/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Создание заказа'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        return super().form_valid(form)


class ListMyOrdersView(ClientMixin, ListView):
    template_name = 'core/list_my_orders.html'
    extra_context = {'title': 'Список заказов'}
    ordering = '-start_datetime'

    def get_queryset(self):
        return Order.objects.filter(sender=self.request.user)


class ListActualOrdersView(EmployeeMixin, ListView, SingleObjectMixin):
    template_name = 'core/list_actual_orders.html'
    queryset = Order.objects.filter(status=Order.CREATED_TYPE)
    extra_context = {'title': 'Список текущих заказов'}
    ordering = '-start_datetime'

    def get_success_url(self):
        success_url = reverse_lazy('detail_order', pk=self.kwargs['pk'])
        return str(success_url)

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.accept()
        return HttpResponseRedirect(self.get_success_url())


class DetailOrderView(ParticipantMixin, DetailView):
    model = Order
    template_name = 'core/detail_order.html'
    extra_context = {'title': 'Детали заказа'}

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
    extra_context = {'title': 'Create Car'}
