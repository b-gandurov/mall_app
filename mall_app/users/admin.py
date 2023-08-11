from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm
from .models import AppUser, UserProfile

admin.site.register(AppUser)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


class AppUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'new_password', 'confirm_password')}),
        ('Permissions', {'fields': ('is_staff','groups')}),
        # Add other fieldsets as needed
    )
    list_display = ('email', 'is_staff', 'is_active')  # Modify as needed
    ordering = ('email',)  # Modify as needed

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = CustomUserChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AppUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(AppUser)
admin.site.register(AppUser, AppUserAdmin)

# class AppUserAdmin(UserAdmin):
#     inlines = (UserProfileInline,)
#     form = CustomUserChangeForm
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         # Add other fieldsets as needed
#     )
#     list_display = ('email', 'is_staff', 'is_active')  # Add other fields as needed
#     ordering = ('email',)
#
#     def get_form(self, request, obj=None, **kwargs):
#         if request.user.is_superuser:
#             kwargs['form'] = CustomUserChangeForm
#         return super().get_form(request, obj, **kwargs)
#
#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(AppUserAdmin, self).get_inline_instances(request, obj)
#
# admin.site.unregister(AppUser)
# admin.site.register(AppUser, AppUserAdmin)
