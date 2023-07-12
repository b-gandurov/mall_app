from django.contrib import admin
from .models import AppUser, UserProfile

admin.site.register(AppUser)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


class AppUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AppUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(AppUser)
admin.site.register(AppUser, AppUserAdmin)
