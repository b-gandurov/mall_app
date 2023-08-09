from datetime import datetime, timedelta

from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic as views

from django.shortcuts import redirect
from django.views.generic import DeleteView

from mall_app.cinema.models import Ticket
from mall_app.stores.models import Reservation
from mall_app.users.forms import UserProfileForm
from mall_app.users.models import UserProfile
from django.contrib.auth.forms import PasswordResetForm

def sort_reservations_by_remaining_time(reservations):
    # Get the current time
    now = timezone.now()

    # Add a computed property to each reservation representing the remaining time
    for reservation in reservations:
        reservation.remaining_time = (reservation.reservation_time + timedelta(minutes=5)) - now

    # Sort the reservations by the remaining time
    sorted_reservations = sorted(reservations, key=lambda r: (r.remaining_time < timedelta(0), r.remaining_time))

    return sorted_reservations

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





# class UserProfileView(views.UpdateView):
#     model = UserProfile
#     form_class = UserProfileForm
#     template_name = 'user_profile.html'
#     success_url = reverse_lazy('index')
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reservations'] = self.request.user.reservations.all()
#         return context

class UserProfileView(views.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('index')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     reservations = Reservation.objects.filter(user=self.request.user)
    #     sorted_reservations = sort_reservations_by_remaining_time(reservations)
    #     context['reservations'] = sorted_reservations
    #     # context['reservations'] = Reservation.objects.filter(user=self.request.user)
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        claimed_reservations = Reservation.objects.filter(user=self.request.user, is_claimed=True)
        unclaimed_reservations = Reservation.objects.filter(user=self.request.user, is_claimed=False)
        sorted_unclaimed_reservations = sort_reservations_by_remaining_time(unclaimed_reservations)
        # Create a Paginator object
        paginator = Paginator(sorted_unclaimed_reservations, 3)  # 3 items per page
        page_unclaimed = self.request.GET.get('page_unclaimed', 1)  # Get the page number from the request
        unclaimed_reservations_page = paginator.get_page(page_unclaimed)

        paginator_claimed = Paginator(claimed_reservations, 3)
        page_claimed = self.request.GET.get('page_claimed', 1)
        claimed_reservations_page = paginator_claimed.get_page(page_claimed)

        user_profile = UserProfile.objects.get(user=self.request.user)

        context['booked_tickets'] = Ticket.objects.filter(customer=user_profile).select_related('seat', 'screening')
        context['claimed_reservations'] = claimed_reservations_page
        context['unclaimed_reservations'] = unclaimed_reservations_page
        return context

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(UserProfileView, self).get_initial()

        # Update the dictionary with the UserProfile field values
        user_profile = self.get_object()
        initial['first_name'] = user_profile.first_name
        initial['last_name'] = user_profile.last_name
        initial['date_of_birth'] = user_profile.date_of_birth
        initial['phone_number'] = user_profile.phone_number

        return initial

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class LogoutUserView(auth_views.LogoutView):
    next_page = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        return redirect('profile')


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    success_url = reverse_lazy('index')
    template_name = 'profile_confirm_delete.html'

    def get_object(self):
        return self.request.user


class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        """Return matching user objects for the given email."""
        email_field_name = get_user_model().EMAIL_FIELD
        for user in get_user_model()._default_manager.filter(**{
                '%s__iexact' % email_field_name: email}):
            if user.has_usable_password() and user.email_user:
                yield user
        else: # Add this line
            self.add_error(None, "Email is not registered") # And this line


def increase_item_quantity(request):
    reservation_id = request.GET.get('reservation_id')
    reservation = Reservation.objects.get(id=reservation_id)

    # Check whether the item's quantity has already been increased
    if not reservation.item_quantity_increased:
        item = reservation.item
        item.quantity += 1
        item.save()
        # Set the flag to True to indicate that the item's quantity has been increased
        reservation.item_quantity_increased = True
        reservation.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'already_increased'})
