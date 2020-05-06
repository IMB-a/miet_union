from django.urls import path

from .views import (
    commissions,
    help_prof_org,
    normative_documents,
    personal_data_protection,
    useful_links,
)

urlpatterns = [
    path('commissions', commissions, name='commissions'),
    path('help_prof_org', help_prof_org, name='help_prof_org'),
    path('normative_documents', normative_documents,
         name='normative_documents'),
    path('personal_data_protection', personal_data_protection,
         name='personal_data_protection'),
    path('useful_links', useful_links, name='useful_links'),
]
