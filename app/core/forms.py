from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.gis.forms import MultiPointField, OSMWidget
from django.db.models import Q
from django.forms import ValidationError

from app.core.models import Order


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'passport', 'country', 'phone_number')


class LogInForm(forms.ModelForm):
    phone_or_email = forms.CharField()
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        value = self.cleaned_data.get('phone_or_email')
        users = get_user_model().objects.filter(Q(email=value) | Q(phone_number=value)).distinct()
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
    from_to_points = MultiPointField(widget=OSMWidget(attrs={'map_width': 800, 'map_height': 500, 'default_zoom': 4}))

    class Meta:
        model = Order
        fields = ('from_to_points', 'mass', 'cargo_features', 'recipient')

    def clean_from_to_points(self):
        value = self.cleaned_data['from_to_points']
        if len(value) < 2:
            raise ValidationError('Order must has 2 points on map')
        return value

    def save(self, commit=True):
        point1 = self.cleaned_data['from_to_points'][0]
        point2 = self.cleaned_data['from_to_points'][1]
        price = round(point1.distance(point2) * self.cleaned_data['mass'] / 1000 + len(self.cleaned_data['cargo_features']) * 100, 2)
        self.instance.price = price
        return super().save(commit)
