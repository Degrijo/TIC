from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from app.core.forms import SignUpClientForm, SignUpEmployeeForm, LogInForm

# Главная страница, Регистрация Клиента (имя, фамилия, пароль, паспорт, страна, номер телефона, почта),
# Вход Клиента (номер телефона/почта, пароль), Регистрация работника (имя, фамилия, пароль, номер телефона, страна
# почта), Вход работника (номер телефона/почта, пароль), # Личный кабинет (имя, фамилия, страна,
# заказы с деталями),
# Оформление заказа для Клиента (типы грузов, масса, начальная и конечная точки), Список прошлых заказов Клиента
# (откуда, куда, ссылка на детали, время начала и конца), Список актуальных заказов для Работника, Детали заказа (отслеживание)


class MainPageView(TemplateView):
    template_name = 'core/main_page.html'


class SignUpClientView(FormView):
    template_name = 'core/signup_client.html'
    form_class = SignUpClientForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInView(FormView):
    template_name = 'core/login.html'
    form_class = LogInForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignUpEmployeeView(FormView):
    template_name = 'core/signup_employee.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class OrderingView(FormView):
    template_name = ''
