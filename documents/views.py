from django.shortcuts import render

from documents.models import (
    CommissionsOfProfcom,
    HelpForProforg,
    HelpForStudentProforg,
    NormativeDocuments,
    ProtectionOfPersonalInformation,
    TheMainActivitiesOfProforg,
    UsefulLinks,
)


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
