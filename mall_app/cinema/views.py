from django.contrib import messages
from django.db import models
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
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
            Prefetch('schedule_set', queryset=Schedule.objects.order_by('show_time').prefetch_related('ticket_set__seat'))
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

        # Count the number of tickets the user has already booked
        user_ticket_count = Ticket.objects.filter(customer=user_profile).count()

        for seat_id in selected_seats:
            seat = get_object_or_404(HallSeat, id=seat_id)

            if user_ticket_count < 6:  # Only allow booking if the user has less than 6 tickets
                if seat.user is None:  # make sure the seat is not already booked
                    seat.user = user
                    seat.save()

                    Ticket.objects.create(
                        customer=user_profile,  # user.profile is your UserProfile instance
                        seat=seat,
                        screening=screening
                    )
                    user_ticket_count += 1  # Increase the count for each ticket booked
            else:
                messages.error(request, "You cannot book more than 6 tickets.")

        return redirect('cinema_schedule')  # Or wherever you want to redirect after booking

# class CinemaView(View):
#     template_name = 'cinema.html'
#
#     def get(self, request, *args, **kwargs):
#         schedules = Schedule.objects.all().prefetch_related('hall', 'movie')
#
#         # Add hall seats to each schedule
#         for schedule in schedules:
#             schedule.seats = HallSeat.objects.filter(hall=schedule.hall)
#
#         return render(request, self.template_name, {'schedules': schedules})
#
#
#
# class BookSeatsView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         # Parse seat IDs from the POST data
#         seat_ids = request.POST.getlist('seats')
#
#         # Get the seats from the database
#         seats = HallSeat.objects.filter(id__in=seat_ids)
#
#         # Check that the right number of seats was found
#         if len(seats) != len(seat_ids):
#             raise Http404("One or more of the selected seats was not found.")
#
#         # Check that none of the seats are already booked
#         for seat in seats:
#             if seat.is_booked:
#                 return JsonResponse({
#                     'error': f'Seat {seat.id} is already booked.',
#                 }, status=400)
#
#         # Book the seats
#         for seat in seats:
#             seat.is_booked = True
#             seat.user = request.user
#             seat.save()
#
#         return JsonResponse({
#             'success': f'Successfully booked {len(seats)} seats.',
#         })