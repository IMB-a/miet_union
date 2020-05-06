from admin_tools.dashboard import Dashboard
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from miet_union.models import (
    EmailSubscription,
    News,
    User,
    Worker,
)


class CustomDashboard(Dashboard):
    colomns = 3
    title = ('Profcom - admin console')

    def __init__(self, **kwargs):
        Dashboard.__init__(**kwargs)


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
    list_display = ('email',
                    'first_name',
                    'middle_name',
                    'last_name',)
    list_filter = ('date_joined',
                   'is_account_confirmed',
                   'is_email_subscription_confirmed')


class EmailSubscriptionAdmin(admin.ModelAdmin):
    class Meta:
        model = Worker
    list_display = ('email',
                    'is_confirmed',
                    'created',
                    )
    list_filter = ('is_confirmed', 'created')


class NewsAdmin(SummernoteModelAdmin):
    class Meta:
        model = News
    summernote_fields = 'main_text'
    fields = ['title', 'main_text', 'image', 'created']
    list_display = ('title',
                    'created',)
    list_filter = ('created',)
    list_per_page = 15


class WorkerAdmin(admin.ModelAdmin):
    class Meta:
        model = Worker
    list_display = ('first_name',
                    'last_name',
                    'middle_name',
                    'position',
                    'phone_num',
                    'email',
                    'photo',
                    )
    list_filter = ('last_name', 'first_name')


admin.site.index_title = ('Профком')
admin.site.site_title = ('Административная консоль')


admin.site.register(EmailSubscription, EmailSubscriptionAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Worker, WorkerAdmin)
