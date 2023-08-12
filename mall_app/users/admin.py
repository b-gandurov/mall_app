from django.contrib import admin
from .forms import CustomUserChangeForm
from .models import AppUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fk_name = 'user'


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'new_password', 'confirm_password')}),
        ('Permissions', {'fields': ('is_super', 'is_staff', 'groups',)}),
    )
    list_display = ('email', 'is_staff', 'is_active')
    ordering = ('email',)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = CustomUserChangeForm
        return super().get_form(request, obj, **kwargs)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
