from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.core.forms import SignUpClientForm, SignUpEmployeeForm, LogInForm, CreateOrderForm

# Главная страница, Регистрация Клиента (имя, фамилия, пароль, паспорт, страна, номер телефона, почта),
# Вход Клиента (номер телефона/почта, пароль), Регистрация работника (имя, фамилия, пароль, номер телефона, страна
# почта), Вход работника (номер телефона/почта, пароль), # Личный кабинет (имя, фамилия, страна,
# заказы с деталями),
# Оформление заказа для Клиента (типы грузов, масса, начальная и конечная точки), Список прошлых заказов Клиента
# (откуда, куда, ссылка на детали, время начала и конца), Список актуальных заказов для Работника, Детали заказа (отслеживание)


class MainPageView(TemplateView):
    template_name = 'core/main_page.html'
    extra_context = {'title': 'Main Page'}


class SignUpClientView(FormView):
    template_name = 'core/signup_client.html'
    form_class = SignUpClientForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up Client'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInView(FormView):
    template_name = 'core/login_employee.html'
    form_class = LogInForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Log In'}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignUpEmployeeView(FormView):
    template_name = 'core/signup_employee.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up Employee'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CreateOrderView(FormView, LoginRequiredMixin):
    template_name = 'core/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Create Order'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        return super().form_valid(form)
