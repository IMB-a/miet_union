import logging

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string

from miet_union import settings
from miet_union.forms import (
    EmailingForm
)
from miet_union.models import (
    EmailSubscription,
    User,
)


logger = logging.getLogger(__name__)


def reset_password_page(request):
    """
    Set new password
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    email_form = EmailingForm(request.POST or None)
    if email_form.is_valid():
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            secret_key = User.objects.get(email=email).secret_key
            context.update({'secret_key': secret_key})
            try:
                send_mail(
                    subject='Изменение пароля',
                    message="",
                    html_message=render_to_string(
                        'miet_union/email_reset_password.html', context),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except NameError:
                logger.error('''EMAIL_HOST_USER not found in
                    send_mail_to_subscribe_confirm''')

            messages.success(request, f'''Выслано письмо на
                    {email} для изменения пароля''')
    context.update({'email_form': email_form})

    return render(request, 'miet_union/reset_password_page.html', context)


def send_mail_to_subscribe_confirm(email, is_registred_user):
    """
    Send emails to accounts with
    EmailSubscription.is_confirmed is True
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    if is_registred_user:
        user = User.objects.get(email=email)
        context.update({'secret_key': user.secret_key})
    else:
        email_instance = EmailSubscription.objects.get(email=email)
        context.update({'secret_key': email_instance.secret_key})
    try:
        send_mail(
            subject='Подтверждение подписки',
            message="""Пожалуйста подтвердите подписку на рассылку
                    новостей от профкома МИЭТ""",
            html_message=render_to_string(
                'miet_union/email_subscribe_confirm.html', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except NameError:
        logger.error('''EMAIL_HOST_USER not found in
            send_mail_to_subscribe_confirm''')


def send_mail_to_account_confirm(email):
    """
    Send emails to accounts with
    EmailSubscription.is_confirmed is True
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    user = User.objects.get(email=email)
    context.update({'secret_key': user.secret_key})
    try:
        send_mail(
            subject='Подтверждение email на сайте профкома МИЭТ',
            message="Пожалуйста подтвердите email для активации аккаунта",
            html_message=render_to_string(
                'miet_union/email_user_confirm.html', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except NameError:
        logger.error('''EMAIL_HOST_USER not found in
            send_mail_to_subscribe_confirm''')


def send_reset_password_email(email):
    """
    Send emails to for password reset
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    user = User.objects.get(email=email)
    context.update({'secret_key': user.secret_key})
    try:
        send_mail(
            subject='Подтверждение email на сайте профкома МИЭТ',
            message="Пожалуйста подтвердите email для активации аккаунта",
            html_message=render_to_string(
                'miet_union/email_reset_password.html', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except NameError:
        logger.error('''EMAIL_HOST_USER not found in
            send_mail_to_subscribe_confirm''')
