from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import check_password

from miet_union.services.send_emails import (
    send_mail_to_subscribe_confirm,
    send_mail_to_account_confirm,
)
from miet_union.services.subscribing import unsubscribe_emailing
from miet_union.models import (
    EmailSubscription,
    News,
    User,
)


def validate_email_form(request, email_form, context):
    if email_form.is_valid():
        email = request.POST.get('email')
        if email:
            if EmailSubscription.objects.filter(email=email):
                if EmailSubscription.objects.get(email=email
                                                 ).is_confirmed is True:
                    messages.error(request, 'Вы уже подписаны')
                else:
                    messages.info(request, '''Вы уже отправляли заявку,
                                            выслана новая.''')
                    # send an e-mail to an unregistered user
                    send_mail_to_subscribe_confirm(
                        email, is_registred_user=False)
            elif User.objects.filter(email=email):
                if User.objects.get(
                        email=email).is_email_subscription_confirmed is True:
                    messages.error(request, 'Вы уже подписаны')
                else:
                    # send email to
                    # User.is_email_subscription_confirmed = False
                    send_mail_to_subscribe_confirm(
                        email=email, is_registred_user=True)
                    messages.info(request, '''Заявка отправлена''')
            else:
                new_email = EmailSubscription.objects.create(email=email)
                new_email.save()
                # send an e-mail to an unregistered user
                send_mail_to_subscribe_confirm(
                    new_email.email, is_registerd_user=False)
                messages.error(request, 'Заявка отправлена')
    context.update({'email_form': email_form})
    return context


def validate_search_news_form(request, search_news_form,
                              email_form, context):
    res_news_context = {}
    if search_news_form.is_valid():
        str_input = request.POST.get('str_input')
        if str_input:
            title_res, main_text_res = News.search_news(str_input)
            res_news_context.update({'title_res': title_res,
                                     'main_text_res': main_text_res,
                                     'search_news_form': search_news_form,
                                     'email_form': email_form})
    return res_news_context


def validate_user_login_form(request, user_login_form):
    if user_login_form.is_valid():
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(email=email.strip(),
                                password=password.strip())
            if user:
                login(request, user)
                rederict_path = 'home'
                return rederict_path
            else:
                messages.error(request, 'Неправельный логин или пароль')
                return None


def validate_registration_form(request, registration_form):
    if registration_form.is_valid():
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        rank = request.POST.get('rank')
        user = User.objects.none()
        if email and password and first_name and last_name and \
                middle_name and rank:
            if not User.objects.filter(email=email):
                user = User.objects.create_user(email=email,
                                                first_name=first_name,
                                                middle_name=middle_name,
                                                last_name=last_name,
                                                password=password,
                                                is_active=True,
                                                rank=rank,
                                                is_staff=False,
                                                is_admin=False)
                user.save()
                send_mail_to_account_confirm(user.email)
                # login after registration
                user = authenticate(email=email.strip(),
                                    password=password.strip())
                login(request, user)
                messages.info(request, '''Пожалуйста,
                    подтвердите акканут на почте.
                    Иначе не сможите восстановить пароль.''')
                return '/my_account'
            else:
                messages.error(request, 'Этот email уже занят')
                return '/login'


def validate_financial_assistance_form(request, financial_assistance_form,
                                       rank, context):
    if financial_assistance_form.is_valid():
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        middle_name = request.GET.get('middle_name')
        if User.objects.filter(first_name=first_name,
                               last_name=last_name,
                               middle_name=middle_name,
                               rank=rank):
            res = User.objects.get(first_name=first_name,
                                   last_name=last_name,
                                   middle_name=middle_name,
                                   rank=rank).financial_assistance_status
            context.update({'res': res, 'rank': rank})
        else:
            context.update({'rank': rank})
    context.update({'financial_assistance_form': financial_assistance_form})
    return context


def validate_password_reset_form(request, secret_key,
                                 password_reset_form, context):
    if password_reset_form.is_valid():
        password = request.POST.get('password')
        confirmed_password = request.POST.get('confirmed_password')
        if password == confirmed_password:
            if User.objects.filter(secret_key=secret_key):
                user = User.objects.get(secret_key=secret_key)
                user.set_password(password)
                user.save()
                messages.success(request, 'Пароль изменен')
                return 'home'
        else:
            messages.error(request, 'Пароли не совпадают')
            return f'/reset_password/{secret_key}'


def validate_change_password_form(request, change_password_form, context):
    user = User.objects.get(email=request.user.email)
    current_password_from_requst = request.user.password
    if change_password_form.is_valid():
        current_password_from_form = request.POST.get(
            "current_password")
        new_password = request.POST.get("new_password")
        confirmed_new_password = request.POST.get("confirmed_new_password")
        matchcheck = check_password(current_password_from_form,
                                    current_password_from_requst)
        if matchcheck:
            if new_password == confirmed_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль изменен')
            else:
                messages.error(request, 'Пароли не совпадают')
        else:
            messages.error(request, 'Неправельный пароль')


def validate_email_form_in_my_account(request, email_form,
                                      email_unsubscribe_form, context):

    user = User.objects.get(email=request.user.email)

    if user.is_email_subscription_confirmed:
        context.update({'email_unsubscribe_form': email_unsubscribe_form})
        if email_unsubscribe_form.is_valid():
            unsubscribe_emailing(user.secret_key, is_registred_user=True)
            messages.success(request, 'Вы успешно отписались')
            return '/my_account'
    else:
        context.update({'email_form': email_form})
        if email_form.is_valid():
            send_mail_to_subscribe_confirm(user.email, is_registred_user=True)
            messages.info(request, 'Заявка отправлена.')
            return '/my_account'
    return None
