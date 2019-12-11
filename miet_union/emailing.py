from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from miet_union import settings

def send_email(email):
    send_mail(
        subject='Test email',
        message='Hello from django.',
        # text_content = 'This is an important message.',
        html_message='<p>This is an <strong>important</strong> message.</p>',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

