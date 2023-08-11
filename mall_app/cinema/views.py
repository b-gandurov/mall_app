from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from mall_app.cinema.models import Schedule, Movie, HallSeat, Ticket
from mall_app.users.models import UserProfile


class CinemaScheduleView(ListView):
    model = Movie
    template_name = 'schedule.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('schedule_set',
                     queryset=Schedule.objects.order_by('show_time').prefetch_related('ticket_set__seat'))
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booked_seats = {}
        for movie in context['movies']:
            for schedule in movie.schedule_set.all():
                booked_seats[schedule.id] = [ticket.seat.id for ticket in schedule.ticket_set.all()]
        context['booked_seats'] = booked_seats
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        selected_seats = request.POST.getlist('seats')
        screening_id = request.POST.get('screening')

        screening = get_object_or_404(Schedule, id=screening_id)
        user_ticket_count = Ticket.objects.filter(customer=user_profile).count()

        for seat_id in selected_seats:
            seat = get_object_or_404(HallSeat, id=seat_id)

            if user_ticket_count < 6:
                if seat.user is None:
                    seat.user = user
                    seat.save()

                    Ticket.objects.create(
                        customer=user_profile,
                        seat=seat,
                        screening=screening
                    )
                    user_ticket_count += 1
            else:
                messages.error(request, "You cannot book more than 6 tickets.")

        return redirect('cinema_schedule')


class UnbookSeatView(View):
    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id, customer__user=request.user)

        seat = ticket.seat
        seat.user = None
        seat.save()

        ticket.delete()

        messages.success(request, "Seat unbooked successfully.")
        return redirect('profile')
