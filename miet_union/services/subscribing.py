from django.contrib import messages
from django.shortcuts import redirect

from miet_union.models import (
    EmailSubscription,
    User,
)


def unsubscribe_emailing(secret_key, is_registred_user):
    """
    Set is_email_subscription_confirmed to False
    or delete EmailSubscription instance from db
    """
    if is_registred_user:
        User.objects.filter(secret_key=secret_key).update(
            is_email_subscription_confirmed=False)
        user = User.objects.get(secret_key=secret_key)
        # also for unregistered users with same email
        if EmailSubscription.objects.filter(email=user.email):
            EmailSubscription.objects.filter(email=user.email).delete()
        return redirect('home')
    else:
        EmailSubscription.objects.filter(secret_key=secret_key).delete()


def subscribe_confirm(request, secret_key):
    """
    Confirm Subscription: EmailSubscription.is_confirmed = True
    """
    if User.objects.filter(secret_key=secret_key):
        user = User.objects.filter(secret_key=secret_key)
        user.update(is_email_subscription_confirmed=True)
    EmailSubscription.objects.filter(
        secret_key=secret_key).update(is_confirmed=True)
    messages.success(request, 'Вы успешно подписались')
    return redirect('home')
