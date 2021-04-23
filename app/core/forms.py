from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import ValidationError

# имя, фамилия, пароль, паспорт, страна, номер телефона, почта
from app.core.models import Order


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Optional.')
    last_name = forms.CharField(max_length=30, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=12, initial='+')

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'passport', 'country', 'phone_number')

    def clean_phone_number(self):
        value = self.cleaned_data.get('phone_number')
        if not value.startswith('+'):
            raise ValidationError('Phone number must start with +')
        return value


class LogInForm(forms.ModelForm):
    phone_or_email = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        value = self.cleaned_data.get('phone_or_email')
        users = get_user_model().objects.filter(Q(email=value) | Q(phone_number=value[1:])).distinct()
        if users.count() != 1:
            raise ValidationError({'phone_or_email': 'No such phone or email for signed up users'})
        user = users.first()
        if not user.check_password(self.cleaned_data.get('password')):
            raise ValidationError({'password': 'Wrong password'})
        self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    class Meta:
        model = get_user_model()
        fields = ('phone_or_email', 'password')


class SignUpEmployeeForm(SignUpForm):
    def save(self, commit=True):
        data = self.cleaned_data
        data.pop('password2')
        return self.Meta.model.objects.create_employee(**data)


class SignUpClientForm(SignUpForm):
    def save(self, commit=True):
        data = self.cleaned_data
        data.pop('password2')
        return self.Meta.model.objects.create_client(**data)


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('start_point', 'end_point', 'price', 'mass', 'cargo_features', 'recipient')
