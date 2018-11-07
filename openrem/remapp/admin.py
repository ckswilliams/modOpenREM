from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from .models import UserProfile, NotPatientIndicatorsName, NotPatientIndicatorsID, AdminTaskQuestions


admin.site.register(AdminTaskQuestions)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.site_url = reverse_lazy('home')


@admin.register(NotPatientIndicatorsID)
class NotPatientIndicatorsIDAdmin(admin.ModelAdmin):
    list_display = ('not_patient_id', )
    list_editable = ('not_patient_id', )
    view_on_site = False


@admin.register(NotPatientIndicatorsName)
class NotPatientIndicatorsNameAdmin(admin.ModelAdmin):
    list_display = ('not_patient_name', )
    list_editable = ('not_patient_name', )
    view_on_site = False


admin.site.site_header = u'OpenREM Site Administration'
admin.site.site_title = u'OpenREM Site Administration'
