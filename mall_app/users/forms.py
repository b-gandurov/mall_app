from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm
from mall_app.users.models import UserProfile
from django.contrib.auth import forms as auth_forms

UserModel = get_user_model()


# class PasswordChangeMixin:
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['new_password'] = forms.CharField(widget=forms.PasswordInput(), required=False,
#                                                       label="New Password")
#         self.fields['confirm_password'] = forms.CharField(widget=forms.PasswordInput(), required=False,
#                                                           label="Confirm New Password")
#
#     def clean_password(self):
#         new_password = self.cleaned_data.get("new_password")
#         confirm_password = self.cleaned_data.get("confirm_password")
#
#         if new_password or confirm_password:
#             if new_password != confirm_password:
#                 raise ValidationError("The new passwords do not match")
#             validate_password(new_password, self.instance)
#
#         return new_password
#
#     def save_password(self, user):
#         new_password = self.cleaned_data.get("new_password")
#
#         if new_password:
#             user.set_password(new_password)
#             user.save()
#
#
# class UserProfileForm(PasswordChangeMixin, forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ('user',)
#
#     def clean(self):
#         cleaned_data = super().clean()
#         self.clean_password()
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = self.instance.user
#         self.save_password(user)
#         return super().save(commit=commit)
#
#
# class CustomUserChangeForm(PasswordChangeMixin, forms.ModelForm):
#
#     class Meta(UserChangeForm.Meta):
#         model = get_user_model()
#
#     def clean(self):
#         cleaned_data = super().clean()
#         self.clean_password()
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = self.instance
#         self.save_password(user)
#         return super().save(commit=commit)


# The rest of your forms remain the same


class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm New Password")

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError("The new passwords do not match")
            validate_password(new_password, self.instance.user)

        return cleaned_data

    def save(self, commit=True):
        user = self.instance.user
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.set_password(new_password)
            user.save()

        return super().save(commit=commit)


class CustomUserChangeForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm New Password")

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        exclude = ('password',)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError("The new passwords do not match")
            validate_password(new_password, self.instance)

        return cleaned_data

    def save(self, commit=True):
        user = self.instance
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.set_password(new_password)
            user.save()

        return super().save(commit=commit)


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Return matching user objects for the given email."""
        email_field_name = get_user_model().EMAIL_FIELD
        for user in get_user_model()._default_manager.filter(**{
            '%s__iexact' % email_field_name: email}):
            if user.has_usable_password() and user.email_user:
                yield user
        else:
            self.add_error(None, "Email is not registered")


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
