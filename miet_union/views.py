import logging

from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from miet_union import settings
from .forms import (
    ChangePasswordForm,
    EmailingForm,
    EmailingUnsubscribeForm,
    SearchNewsForm,
    StudentFinancialAssistanceForm,
    UserLoginForm,
    UserRegistrationForm,
)
from .models import (
    CommissionsOfProfcom,
    EmailSubscription,
    HelpForProforg,
    HelpForStudentProforg,
    News,
    NormativeDocuments,
    ProtectionOfPersonalInformation,
    TheMainActivitiesOfProforg,
    UsefulLinks,
    Worker,
    User,
)

logger = logging.getLogger(__name__)


def home(request):
    context = {}
    all_news = News.objects.all()
    paginator = Paginator(all_news, 5)
    news_count = 0
    for news in all_news:
        news_count += 1
    context.update({'news_count': news_count})
    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        all_news = paginator.page(1)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)
    context.update({'all_news': all_news})

    email_form = EmailingForm(request.POST or None)
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
                    send_mail_to_subscribe_confirm(email)
            elif User.objects.filter(email=email):
                if User.objects.get(
                        email=email).is_email_subscription_confirmed is True:
                    messages.error(request, 'Вы уже подписаны')
            else:
                new_email = EmailSubscription.objects.create(email=email)
                new_email.save()
                send_mail_to_subscribe_confirm(new_email.email)
    context.update({'email_form': email_form})

    search_news_form = SearchNewsForm(request.POST or None)
    if search_news_form.is_valid():
        res_news_context = {}
        str_input = request.POST.get('str_input')
        if str_input:
            title_res, main_text_res = News.search_news(str_input)
            res_news_context.update({'title_res': title_res,
                                     'main_text_res': main_text_res,
                                     'search_news_form': search_news_form,
                                     'email_form': email_form})
            return render(request,
                          'miet_union/search_news.html',
                          res_news_context)
    context.update({'search_news_form': search_news_form})

    return render(request, 'miet_union/home.html', context)


def our_team(request):
    worker = Worker.objects.all()
    context = {
        'worker': worker,
    }
    return render(request, 'miet_union/our_team.html', context)


def registration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        rank = request.POST.get('rank')
        user = User.objects.none()
        if not User.objects.get(email=email):
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
            # login after registration
            user = authenticate(email=email.strip(),
                                password=password.strip())
            login(request, user)
            return redirect('/my_account')
        else:
            messages.error(request, 'Этот email уже занят')

    return render(request, "miet_union/registration.html", {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email.strip(),
                            password=password.strip())
        if user:
            login(request, user)
            next_post = request.POST.get('next')
            rederict_path = next_ or next_post or '/'
            return redirect(rederict_path)
        else:
            messages.error(request, 'Неправельный логин или пароль')
    return render(request, 'miet_union/login.html', {'form': form})


@login_required
def my_account(request):
    context = {}
    change_password_form = ChangePasswordForm(request.POST or None)
    context.update({'change_password_form': change_password_form})
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

    email_form = EmailingForm(request.POST or None)
    user = User.objects.get(email=request.user.email)
    email_unsubscribe_form = EmailingUnsubscribeForm(
        request.POST or None)

    if user.is_email_subscription_confirmed:
        context.update({'email_unsubscribe_form': email_unsubscribe_form})
        if email_unsubscribe_form.is_valid():
            unsubscribe_emailing(user.secret_key, is_registred_user=True)
            messages.success(request, 'Вы успешно отписались')
            return redirect('/my_account')
    else:
        context.update({'email_form': email_form})
        if email_form.is_valid():
            send_mail_to_subscribe_confirm(user.email, is_registred_user=True)
            messages.info(request, 'Заявка отправлена.')
            return redirect('/my_account')

    return render(request, 'miet_union/my_account.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def news_page(request, pk):
    context = {}
    news = get_object_or_404(News, pk=pk)
    context.update({'news': news})
    email_form = EmailingForm(request.POST or None)
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
                    send_mail_to_subscribe_confirm(email)
            else:
                new_email = EmailSubscription.objects.create(email=email)
                new_email.save()
                send_mail_to_subscribe_confirm(new_email.email,
                                               is_registred_user=False)
    context.update({'email_form': email_form})

    search_news_form = SearchNewsForm(request.POST or None)
    if search_news_form.is_valid():
        res_news_context = {}
        str_input = request.POST.get('str_input')
        if str_input:
            title_res, main_text_res = News.search_news(str_input)
            res_news_context.update({'title_res': title_res,
                                     'main_text_res': main_text_res,
                                     'search_news_form': search_news_form,
                                     'email_form': email_form})
            return render(request,
                          'miet_union/search_news.html',
                          res_news_context)
    context.update({'search_news_form': search_news_form})

    return render(request, 'miet_union/news_page.html', context)


def error_400(request, exception):
    return render(request, 'miet_union/400.html')


def error_403(request, exception):
    return render(request, 'miet_union/403.html')


def error_404(request, exception):
    return render(request, 'miet_union/404.html')


def error_500(request):
    return render(request, 'miet_union/500.html')


def test(request):
    return render(request, 'miet_union/test.html')


def social_card(request):
    return render(request, 'miet_union/social_card.html')


def help_prof_org(request):
    help_prof_org_documents = HelpForProforg.objects.all()
    help_student_prof_org_documents = HelpForStudentProforg.objects.all()
    the_main_activities_of_prof_org_documents = TheMainActivitiesOfProforg.objects.all()  # noqa
    context = {
        'help_prof_org_documents': help_prof_org_documents,
        'help_student_prof_org_documents': help_student_prof_org_documents,
        'the_main_activities_of_prof_org_documents': the_main_activities_of_prof_org_documents,  # noqa
    }
    return render(request, 'miet_union/help_prof_org.html', context)


def prof_com(request):
    return render(request, 'miet_union/prof_com.html')


def prof_souz(request):
    return render(request, 'miet_union/prof_souz.html')


def financial_assistance(request, rank):
    context = {}
    form = StudentFinancialAssistanceForm(request.GET or None)
    if form.is_valid():
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
    context.update({'form': form})
    return render(request,
                  'miet_union/financial_assistance.html',
                  context)


def test_404(request):
    return render(request, 'miet_union/404.html')


def commissions(request):
    commissions_of_profcom_docunets = CommissionsOfProfcom.objects.all()
    context = {
        'commissions_of_profcom_docunets': commissions_of_profcom_docunets,
    }
    return render(request, 'miet_union/commissions.html', context)


def normative_documents(request):
    normative_documents = NormativeDocuments.objects.all()
    context = {
        'normative_documents': normative_documents,
    }
    return render(request, 'miet_union/normative_documents.html', context)


def personal_data_protection(request):
    protection_of_personal_information_documents = ProtectionOfPersonalInformation.objects.all()    # noqa
    context = {
        'protection_of_personal_information_documents': protection_of_personal_information_documents,   # noqa
    }
    return render(request, 'miet_union/personal_data_protection.html', context)


def useful_links(request):
    useful_links_documents = UsefulLinks.objects.all()
    context = {
        'useful_links_documents': useful_links_documents,
    }
    return render(request, 'miet_union/useful_links.html', context)


def unsubscribe_emailing(secret_key, is_registred_user):
    """
    Set is_email_subscription_confirmed to False
    and delete EmailSubscription instance from db
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


def unsubscribe_emailing_in_url(request, secret_key):
    """
    Delete EmailSubscription instance from db
    """
    if User.objects.filter(secret_key=secret_key):
        unsubscribe_emailing(secret_key, is_registred_user=True)
    else:
        unsubscribe_emailing(secret_key, is_registred_user=False)
    messages.success(request, 'Вы успешно отписались')


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
                'miet_union/subscribe_confirm.html', context),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except NameError:
        logger.error('''EMAIL_HOST_USER not found in
            send_mail_to_subscribe_confirm''')
