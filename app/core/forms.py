from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# имя, фамилия, пароль, паспорт, страна, номер телефона, почта


class SignUpClientForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Optional.')
    last_name = forms.CharField(max_length=30, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'passport', 'country', 'phone_number', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.HiddenInput()
        self.fields['role'].initial = get_user_model().CLIENT_ROLE
