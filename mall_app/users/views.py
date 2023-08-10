from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import views as auth_views, login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic as views
from django.shortcuts import redirect
from django.views.generic import DeleteView
from mall_app.cinema.models import Ticket
from mall_app.stores.models import Reservation, Store
from mall_app.users.forms import UserProfileForm, RegisterUserForm
from mall_app.users.models import UserProfile


def sort_reservations_by_remaining_time(reservations):
    now = timezone.now()
    for reservation in reservations:
        reservation.remaining_time = (reservation.reservation_time + timedelta(minutes=5)) - now
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
    stores = Store.objects.all()
    return render(request, 'index.html', {'stores': stores})


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


class UserProfileView(LoginRequiredMixin, views.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        new_password = form.cleaned_data.get('new_password')

        if new_password:
            user = self.request.user
            user.set_password(new_password)
            user.save()
            user.refresh_from_db()
            update_session_auth_hash(self.request, user)
            messages.success(self.request, 'Your password was changed successfully.')  # This line

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        claimed_reservations = Reservation.objects.filter(user=self.request.user, is_claimed=True)
        unclaimed_reservations = Reservation.objects.filter(user=self.request.user, is_claimed=False)
        sorted_unclaimed_reservations = sort_reservations_by_remaining_time(unclaimed_reservations)

        paginator = Paginator(sorted_unclaimed_reservations, 3)
        page_unclaimed = self.request.GET.get('page_unclaimed', 1)
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

        initial = super(UserProfileView, self).get_initial()
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


def increase_item_quantity(request):
    reservation_id = request.GET.get('reservation_id')
    reservation = Reservation.objects.get(id=reservation_id)


    if not reservation.item_quantity_increased:
        item = reservation.item
        item.quantity += 1
        item.save()

        reservation.item_quantity_increased = True
        reservation.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'already_increased'})
