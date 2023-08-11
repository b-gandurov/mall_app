from django.contrib import admin
from .models import Movie, CinemaHall, Schedule, HallSeat, Ticket

admin.site.register(Movie)
admin.site.register(CinemaHall)
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]

admin.site.unregister(Movie)
admin.site.register(Movie, MovieAdmin)


@admin.register(HallSeat)
class HallSeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'row', 'column', 'user']
    list_filter = ['user']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'seat', 'screening']
    list_filter = ['customer', 'screening']