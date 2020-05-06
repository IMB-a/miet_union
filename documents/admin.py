from django.contrib import admin

from documents.models import (
    CommissionsOfProfcom,
    HelpForProforg,
    HelpForStudentProforg,
    NormativeDocuments,
    ProtectionOfPersonalInformation,
    TheMainActivitiesOfProforg,
    UsefulLinks,
)


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


admin.site.register(CommissionsOfProfcom, CommissionsOfProfcomAdmin)
admin.site.register(HelpForProforg, HelpForProforgAdmin)
admin.site.register(HelpForStudentProforg, HelpForStudentProforgAdmin)
admin.site.register(NormativeDocuments, NormativeDocumentsAdmin)
admin.site.register(ProtectionOfPersonalInformation,
                    ProtectionOfPersonalInformationAdmin)
admin.site.register(TheMainActivitiesOfProforg,
                    TheMainActivitiesOfProforgAdmin)
admin.site.register(UsefulLinks, UsefulLinksAdmin)
