from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404


from .forms import (
    EmailingForm,
    StudentMoneyForm,
    UserLoginForm,
    ChangePasswordForm,
)

from documents.models import (
    CommissionsOfProfcom,
    HelpForProforg,
    HelpForStudentProforg,
    NormativeDocuments,
    ProtectionOfPersonalInformation,
    TheMainActivitiesOfProforg,
    UsefulLinks,
)
from news.models import (
    EmailSubscription,
    News,
)
from ourteam.models import Worker

from pdf.pdfed import pdf_money


def home(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 5)

    page = request.GET.get('page')
    try:
        all_news = paginator.page(page)
    except PageNotAnInteger:
        all_news = paginator.page(1)
    except EmptyPage:
        all_news = paginator.page(paginator.num_pages)

    context = {
        'all_news': all_news,
    }

    email_form = EmailingForm(request.POST or None)
    if email_form.is_valid():
        email = request.POST.get('email')
        if email and EmailSubscription.objects.filter(email=email):
            if EmailSubscription.objects.get(email=email):
                messages.error(request, 'Вы уже подписаны')
        else:
            new_email = EmailSubscription.objects.create(email=email)
            new_email.save()
            messages.success(request, 'Вы успешно подписались')
    context.update({'email_form': email_form})

    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        rederict_path = next_ or next_post or '/'
        return redirect(rederict_path)

    context.update({'form': form})
    return render(request, 'miet_union/home.html', context)


def our_team(request):
    worker = Worker.objects.all()
    context = {
        'worker': worker,
    }
    return render(request, 'miet_union/our_team.html', context)


def registration(request):
    form = UserCreationForm(data=request.POST or None)
    next_ = request.GET.get('next')
    if request.method == 'POST' and form.is_valid():
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'   # noqa
        form.save()
        return redirect('/login')

    return render(request, "miet_union/registration.html", {'form': form})


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        rederict_path = next_ or next_post or '/'
        return redirect(rederict_path)
    return render(request, 'miet_union/login.html', {'form': form})


@login_required
def my_account(request):
    change_password_form = ChangePasswordForm(request.POST or None)
    user = User.objects.get(username=request.user)
    current_password_from_requst = request.user.password
    if change_password_form.is_valid():
        current_password_from_form = request.POST.get(
            "current_password")
        new_password = request.POST.get("new_password")
        confirmed_new_password = request.POST.get("confirmed_new_password")
        matchcheck = check_password(current_password_from_requst,
                                    current_password_from_form)
        print(matchcheck)
        if matchcheck:
            if new_password == confirmed_new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль изменен')
            else:
                messages.error(request, 'Пароли не совпадают')
        else:
            messages.error(request, 'Неправельный пароль')
    return render(request, 'miet_union/my_account.html',
                  {'change_password_form': change_password_form})


def logout_view(request):
    logout(request)
    return redirect('home')


def news_page(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'miet_union/news_page.html', {'news': news})


def error_400(request, exception):
    return render(request, 'miet_union/400.html')


def error_403(request, exception):
    return render(request, 'miet_union/403.html')


def error_404(request, exception):
    return render(request, 'miet_union/404.html')


def error_500(request):
    return render(request, 'miet_union/500.html')


def money_help_for_students(request):
    form = StudentMoneyForm(request.POST or None)
    if form.is_valid():
        full_name = request.POST.get('full_name')
        group = request.POST.get('group')
        address = request.POST.get('address')
        reason = request.POST.get('reason')
        date_and_month_of_last_request = request.POST.get(
            'date_and_month_of_last_request')
        year_of_last_request = request.POST.get('year_of_last_request')
        passport_number_part_one = request.POST.get('passport_number_part_one')
        passport_number_part_two = request.POST.get('passport_number_part_two')
        date_of_issue = request.POST.get('date_of_issue')
        place_of_issue = request.POST.get('place_of_issue')
        phone_number = request.POST.get('phone_number')

        pdf_money(
            full_name,
            group,
            address,
            reason,
            date_and_month_of_last_request,
            year_of_last_request,
            passport_number_part_one,
            passport_number_part_two,
            date_of_issue,
            place_of_issue,
            phone_number,
        )
    return render(
        request,
        'miet_union/money_help_for_students.html',
        {"form": form},
    )


def money_help_for_graduate_students(request):
    return render(request, 'miet_union/money_help_for_graduate_students.html')


def money_help_for_workers(request):
    return render(request, 'miet_union/money_help_for_workers.html')


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
