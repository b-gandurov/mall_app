from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, UserChangeForm
from mall_app.users.models import UserProfile
from django.contrib.auth import forms as auth_forms

from mall_app.validators import phone_number_validator

UserModel = get_user_model()


class UserProfileForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm New Password")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(validators=[phone_number_validator])

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
        email_field_name = get_user_model().EMAIL_FIELD
        for user in get_user_model()._default_manager.filter(**{
            '%s__iexact' % email_field_name: email}):
            if user.has_usable_password() and user.email_user:
                yield user
        else:
            self.add_error(None, "Email is not registered")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError(
                    'Please enter a correct email and password. Note that both fields may be case-sensitive.')

        return super(LoginForm, self).clean()


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
