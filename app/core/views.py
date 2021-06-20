from django.contrib.auth import login, get_user_model
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, TemplateView, ListView, UpdateView
from django.views.generic.detail import DetailView

from app.core.forms import SignUpClientForm, SignUpEmployeeForm, LogInForm, CreateOrderForm, AcceptOrderForm
from app.core.mixins import EmployeeMixin, ClientMixin, ParticipantMixin, ContextMixin
from app.core.models import Car, Order


class MainPageView(ContextMixin, TemplateView):
    template_name = 'pages/main_page.html'
    extra_context = {'title': 'Main page'}


class SignUpClientView(ContextMixin, FormView):
    template_name = 'pages/bootstrap_form.html'
    form_class = SignUpClientForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up: client'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogInView(ContextMixin, FormView):
    template_name = 'pages/bootstrap_form.html'
    form_class = LogInForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class SignUpEmployeeView(ContextMixin, FormView):
    template_name = 'pages/bootstrap_form.html'
    form_class = SignUpEmployeeForm
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Sign Up: employee'}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('main_page')


class CreateOrderView(ContextMixin, ClientMixin, FormView):
    template_name = 'pages/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('list_my_orders')
    extra_context = {'title': 'Create order'}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        coors = self.request.user.country_coordinates
        form.fields['from_to_points'].widget.attrs['default_lat'] = coors[0]
        form.fields['from_to_points'].widget.attrs['default_lon'] = coors[1]
        form.fields['recipient'].queryset = get_user_model().objects.filter(role=get_user_model().CLIENT_ROLE)\
                                                                    .exclude(id=self.request.user.id)
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.sender = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)


class ListMyOrdersView(ContextMixin, ListView):
    template_name = 'pages/list_my_orders.html'
    extra_context = {'title': 'List my orders', 'order_model': Order}
    ordering = '-start_datetime'

    def get_queryset(self):
        user = self.request.user
        if user.role == get_user_model().CLIENT_ROLE:
            return Order.objects.filter(sender=user)
        elif user.role == get_user_model().EMPLOYEE_ROLE:
            return Order.objects.filter(employee=user)


class ListActualOrdersView(ContextMixin, EmployeeMixin, ListView):
    template_name = 'pages/list_actual_orders.html'
    queryset = Order.objects.filter(status=Order.CREATED_TYPE)
    success_url = reverse_lazy('list_my_orders')
    extra_context = {'title': 'List actual orders'}
    ordering = '-start_datetime'


class AcceptOrderView(ContextMixin, EmployeeMixin, UpdateView):
    success_url = reverse_lazy('list_my_orders')
    queryset = Order.objects.filter(status=Order.CREATED_TYPE)
    form_class = AcceptOrderForm
    extra_context = {'title': 'Accept order'}
    template_name = 'pages/accept_order.html'

    def form_valid(self, form):
        self.object.accept(self.request.user)
        return super().form_valid(form)


class DetailOrderView(ContextMixin, DetailView):
    model = Order
    template_name = 'pages/detail_order.html'
    extra_context = {'title': 'Order details'}

    def get_success_url(self):
        success_url = reverse_lazy('detail_order', pk=self.kwargs['pk'])
        return str(success_url)


class CreateCarView(ContextMixin, EmployeeMixin, CreateView):
    template_name = 'pages/bootstrap_form.html'
    model = Car
    fields = '__all__'
    success_url = reverse_lazy('main_page')
    extra_context = {'title': 'Create Car'}


class ListCarsView(ContextMixin, EmployeeMixin, ListView):
    template_name = 'pages/list_cars.html'
    model = Car
    extra_context = {'title': 'List cars'}


class FinishOrderView(EmployeeMixin, ParticipantMixin, View):
    model = Order
    success_url = reverse_lazy('list_my_orders')
    object = None

    def get(self, request, *args, **kwargs):
        self.object.finish()
        return HttpResponseRedirect(self.success_url)
