from django.contrib import admin
from .models import Movie, CinemaHall, Schedule, HallSeat, Ticket


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ['hall_name', 'capacity']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]
    list_display = ['movie_name', 'movie_type', 'duration']
    search_fields = ['movie_name', 'movie_type']


@admin.register(HallSeat)
class HallSeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'row', 'column', 'user']
    list_filter = ['user']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'seat', 'screening']
    list_filter = ['customer', 'screening']
