from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from app.core.forms import SignUpClientForm, LogInClientForm, SignUpEmployeeForm, LogInEmployeeForm

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
    success_url = reverse_lazy('signup_client')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInClientView(FormView):
    template_name = 'core/login_client.html'
    form_class = LogInClientForm
    success_url = reverse_lazy('login_client')


    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, phone_number=phone_number, password=password)
        # user = get_user_model().objects.get()
        login(self.request, user)
        return super().form_valid(form)


class SignUpEmployeeView(CreateView):
    template_name = 'core/signup_employee.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('home')


class LogInEmployeeView(FormView):
    template_name = 'core/login_employee.html'
    form_class = LogInEmployeeForm
    success_url = reverse_lazy('home')


class OrderingView(FormView):
    template_name = ''