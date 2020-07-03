import logging

from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from miet_union.forms import (
    ChangePasswordForm,
    EmailingForm,
    EmailingUnsubscribeForm,
    FinancialAssistanceForm,
    PasswordResetForm,
    SearchNewsForm,
    UserLoginForm,
    UserRegistrationForm,
)
from miet_union.models import (
    News,
    Worker,
    User,
)

from miet_union.services.form_validation import (
    validate_change_password_form,
    validate_email_form,
    validate_email_form_in_my_account,
    validate_financial_assistance_form,
    validate_password_reset_form,
    validate_registration_form,
    validate_search_news_form,
    validate_user_login_form,
)
from miet_union.services.news_count import news_count
from miet_union.services.paginator import make_paginator
from miet_union.services.subscribing import unsubscribe_emailing


logger = logging.getLogger(__name__)


def render_home_page(request):
    """
    Render main page with all news
    """
    context = {}
    all_news = News.objects.all()

    context = make_paginator(request, all_news, context)
    context = news_count(all_news, context)

    email_form = EmailingForm(request.POST or None)
    context = validate_email_form(request, email_form, context)

    search_news_form = SearchNewsForm(request.POST or None)
    context.update({'search_news_form': search_news_form})
    res_search_news_context = validate_search_news_form(
        request, search_news_form, email_form, context)
    if res_search_news_context:
        return render(request,
                      'miet_union/search_news.html',
                      res_search_news_context)

    return render(request, 'miet_union/home.html', context)


def render_our_team_page(request):
    context = {'worker': Worker.objects.all()}
    return render(request, 'miet_union/our_team.html', context)


def render_login_page(request):
    user_login_form = UserLoginForm(request.POST or None)
    redirect_url = validate_user_login_form(request, user_login_form)
    if redirect_url:
        return redirect(redirect_url)

    registration_form = UserRegistrationForm(request.POST or None)
    redirect_url = validate_registration_form(request, registration_form)
    if redirect_url:
        return redirect(redirect_url)

    context = {'user_login_form': user_login_form,
               'registration_form': registration_form}
    return render(request, 'miet_union/login.html', context)


@login_required
def render_my_account_page(request):
    context = {}
    change_password_form = ChangePasswordForm(request.POST or None)
    redirect_url = validate_change_password_form(
        request, change_password_form, context)
    if redirect_url:
        return redirect(redirect_url)

    email_form = EmailingForm(request.POST or None)
    email_unsubscribe_form = EmailingUnsubscribeForm(
        request.POST or None)
    redirect_url = validate_email_form_in_my_account(request,
                                                     email_form,
                                                     email_unsubscribe_form,
                                                     context)
    if redirect_url:
        return redirect(redirect_url)

    context.update({'change_password_form': change_password_form})
    return render(request, 'miet_union/my_account.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def render_news_page(request, pk):
    context = {}
    news = get_object_or_404(News, pk=pk)
    context.update({'news': news})

    email_form = EmailingForm(request.POST or None)
    context = validate_email_form(request, email_form, context)

    search_news_form = SearchNewsForm(request.POST or None)
    context.update({'search_news_form': search_news_form})
    res_search_news_context = validate_search_news_form(
        request, search_news_form, email_form, context)
    if res_search_news_context:
        return render(request,
                      'miet_union/search_news.html',
                      res_search_news_context)

    return render(request, 'miet_union/news_page.html', context)


def render_prof_souz_page(request):
    return render(request, 'miet_union/prof_souz.html')


def render_financial_assistance_page(request, rank):
    context = {}
    financial_assistance_form = FinancialAssistanceForm(request.GET or None)
    context = validate_financial_assistance_form(
        request, financial_assistance_form, rank, context)

    return render(request,
                  'miet_union/financial_assistance.html',
                  context)


def test_404(request):
    return render(request, 'miet_union/404.html')


def unsubscribe_emailing_in_url(request, secret_key):
    """
    Set is_email_subscription_confirmed to False
    or delete EmailSubscription instance from db
    """
    if User.objects.filter(secret_key=secret_key):
        unsubscribe_emailing(secret_key, is_registred_user=True)
    else:
        unsubscribe_emailing(secret_key, is_registred_user=False)
    messages.success(request, 'Вы успешно отписались')
    return redirect("home")


def user_confirm(request, secret_key):
    """
    Confirm Subscription: EmailSubscription.is_confirmed = True
    """
    User.objects.filter(secret_key=secret_key
                        ).update(is_account_confirmed=True)
    messages.success(request, 'Вы успешно подтвердили аккаунт')
    return redirect('home')


def reset_password(request, secret_key):
    """
    Set new password
    """
    password_reset_form = PasswordResetForm(request.POST or None)
    context = {'password_reset_form': password_reset_form}
    redirect_url = validate_password_reset_form(request, secret_key,
                                                password_reset_form, context)
    if redirect_url:
        return redirect(redirect_url)
    return render(request, 'miet_union/reset_password_page.html', context)


def render_error_400(request, exception):
    return render(request, 'miet_union/400.html')


def render_error_403(request, exception):
    return render(request, 'miet_union/403.html')


def render_error_404(request, exception):
    return render(request, 'miet_union/404.html')


def render_error_500(request):
    return render(request, 'miet_union/500.html')


def render_social_card_page(request):
    return render(request, 'miet_union/social_card.html')


def render_prof_com_page(request):
    return render(request, 'miet_union/prof_com.html')
