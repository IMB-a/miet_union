from admin_tools.dashboard import Dashboard
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


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
    News,
    EmailSubscription,
)
from ourteam.models import Worker


class CustomDashboard(Dashboard):
    colomns = 3
    title = ('Profcom - admin console')

    def __init__(self, **kwargs):
        Dashboard.__init__(**kwargs)


class EmailSubscriptionAdmin(admin.ModelAdmin):
    class Meta:
        model = Worker
    list_display = ('email',
                    'created'
                    )


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


class HelpForProforgAdmin(admin.ModelAdmin):
    class Meta:
        model = HelpForProforg
    fields = ['title', 'file']
    list_display = ('title',)


class HelpForStudentProforgAdmin(admin.ModelAdmin):
    class Meta:
        model = HelpForStudentProforg
    fields = ['title', 'file']
    list_display = ('title',)


class TheMainActivitiesOfProforgAdmin(admin.ModelAdmin):
    class Meta:
        model = TheMainActivitiesOfProforg
    fields = ['title', 'file']
    list_display = ('title',)


class ProtectionOfPersonalInformationAdmin(admin.ModelAdmin):
    class Meta:
        model = ProtectionOfPersonalInformation
    fields = ['title', 'file']
    list_display = ('title',)


class NormativeDocumentsAdmin(admin.ModelAdmin):
    class Meta:
        model = NormativeDocuments
    fields = ['title', 'file']
    list_display = ('title',)


class CommissionsOfProfcomAdmin(admin.ModelAdmin):
    class Meta:
        model = CommissionsOfProfcom
    fields = ['title', 'file']
    list_display = ('title',)


class UsefulLinksAdmin(admin.ModelAdmin):
    class Meta:
        model = UsefulLinks
    fields = ['title', 'file']
    list_display = ('title',)


admin.site.index_title = ('Профком')
admin.site.site_title = ('Административная консоль')


admin.site.register(EmailSubscription, EmailSubscriptionAdmin)
admin.site.register(CommissionsOfProfcom, CommissionsOfProfcomAdmin)
admin.site.register(HelpForProforg, HelpForProforgAdmin)
admin.site.register(HelpForStudentProforg, HelpForStudentProforgAdmin)
admin.site.register(NormativeDocuments, NormativeDocumentsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(ProtectionOfPersonalInformation,
                    ProtectionOfPersonalInformationAdmin)
admin.site.register(TheMainActivitiesOfProforg,
                    TheMainActivitiesOfProforgAdmin)
admin.site.register(UsefulLinks, UsefulLinksAdmin)
admin.site.register(Worker, WorkerAdmin)
