from django.core.mail import send_mail
from django.template.loader import render_to_string

from miet_union import settings


def send_email(instance, all_emails):
    """
    Send email to all user emails in db
    """
    context = {'ALLOWED_HOSTS': settings.ALLOWED_HOSTS, }
    context.update({'instance': instance})
    all_email_addr = []
    for addr in all_emails:
        all_email_addr.append(addr.email)
    send_mail(
        subject='Новоя новость на сайте профкома института МИЭТ',
        message='Hello from django.',
        # render with dynamic value
        html_message=render_to_string(
            'miet_union/mail_template.html', context),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=all_email_addr,
        fail_silently=False,
    )
