from django.core import validators


class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^\+?1?\d{9,15}$'
    message = "Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed."
