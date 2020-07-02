from django.conf.urls import handler400, handler403, handler404, handler500  # noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from miet_union.services.send_emails import reset_password_page
from miet_union.services.subscribing import subscribe_confirm

from .views import (
    logout_view,
    render_financial_assistance_page,
    render_home_page,
    render_login_page,
    render_my_account_page,
    render_news_page,
    render_our_team_page,
    render_prof_com_page,
    render_prof_souz_page,
    render_social_card_page,
    reset_password,
    test_404,
    unsubscribe_emailing_in_url,
    user_confirm,
)

urlpatterns = [
    path('', render_home_page, name='home'),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('documents/', include('documents.urls')),
    path('favicon.ico', RedirectView.as_view(
        url='/static/images/favicon.ico')),
    path('financial_assistance/<slug:rank>', render_financial_assistance_page,
         name='student_financial_assistance'),
    path('login', render_login_page, name='login'),
    path('logout', logout_view, name='logout'),
    path('my_account', render_my_account_page, name='my_account'),
    path('news/<int:pk>', render_news_page, name='news_page'),
    path('our_team', render_our_team_page, name='our_team'),
    path('prof_com', render_prof_com_page, name='prof_com'),
    path('prof_souz', render_prof_souz_page, name='prof_souz'),
    path('reset_password/<slug:secret_key>',
         reset_password, name='reset_password'),
    path('reset_password_page', reset_password_page,
         name='reset_password_page'),
    path('social_card', render_social_card_page, name='social_card'),
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

handler400 = 'miet_union.views.render_error_400'    # noqa
handler403 = 'miet_union.views.render_error_403'    # noqa
handler404 = 'miet_union.views.render_error_404'    # noqa
handler500 = 'miet_union.views.render_error_500'    # noqa
