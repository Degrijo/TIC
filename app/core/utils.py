from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config.settings.common import EMAIL_HOST_USER


def calculate_price(points_distance, mass, len_cargo_features):
    return round(points_distance * mass / 1000 + len_cargo_features * 100, 2)


def order_mailing(order, template, context, subject):
    for user in (order.sender, order.recipient, order.employee):
        context['user'] = user
        html = render_to_string(template, context)
        plain_message = strip_tags(html)
        send_mail(subject, plain_message, EMAIL_HOST_USER, (user.email,), html_message=html)
