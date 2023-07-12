from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import forms as auth_forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic as views

from django.shortcuts import redirect

from mall_app.users.forms import UserProfileForm
from mall_app.users.models import UserProfile


def anonymous_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


UserModel = get_user_model()


def index(request):
    return render(request, 'index.html')


class RegisterUserForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


class RegisterUserView(views.CreateView):
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        login(self.request, self.object)
        return result

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LoginUserView(auth_views.LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context.pop('form')
        context['log_form_errors'] = bool(context['login_form'].errors)
        return context


class UserProfileView(views.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class LogoutUserView(auth_views.LogoutView):
    pass
