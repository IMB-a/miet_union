from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from .views import (
    financial_assistance,
    home,
    login_view,
    logout_view,
    my_account,
    news_page,
    our_team,
    prof_com,
    prof_souz,
    reset_password,
    reset_password_page,
    social_card,
    subscribe_confirm,
    test_404,
    unsubscribe_emailing_in_url,
    user_confirm,
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('documents/', include('documents.urls')),
    path('favicon.ico', RedirectView.as_view(
        url='/static/images/favicon.ico')),
    path('financial_assistance/<slug:rank>', financial_assistance,
         name='student_financial_assistance'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('my_account', my_account, name='my_account'),
    path('news/<int:pk>', news_page, name='news_page'),
    path('our_team', our_team, name='our_team'),
    path('prof_com', prof_com, name='prof_com'),
    path('prof_souz', prof_souz, name='prof_souz'),
    path('reset_password/<slug:secret_key>',
         reset_password, name='reset_password'),
    path('reset_password_page', reset_password_page,
         name='reset_password_page'),
    path('social_card', social_card, name='social_card'),
    path('subscribe/<slug:secret_key>', subscribe_confirm,
         name='subscribe_confirm'),
    path('summernote/', include('django_summernote.urls')),
    path('test_404', test_404, name='test'),
    path('user_confirm/<slug:secret_key>', user_confirm, name='user_confirm'),
    path('unsubscribe/<slug:secret_key>', unsubscribe_emailing_in_url,
         name='unsubscribe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = 'miet_union.views.error_400'    # noqa
handler403 = 'miet_union.views.error_403'    # noqa
handler404 = 'miet_union.views.error_404'    # noqa
handler500 = 'miet_union.views.error_500'    # noqa
