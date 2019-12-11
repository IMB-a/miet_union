from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string

from miet_union import settings

def send_email(email, context):
    context.update({'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,})
    send_mail(
        subject='Новоя новость на сайте профкома института МИЭТ',
        message='Hello from django.',
        html_message=render_to_string('miet_union/mail_template.html', context), # render with dynamic value
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

