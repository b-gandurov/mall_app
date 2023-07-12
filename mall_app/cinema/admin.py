from django.contrib import admin
from .models import Movie, CinemaHall, Schedule

admin.site.register(Movie)
admin.site.register(CinemaHall)
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1  # number of extra forms to display

class MovieAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline]

admin.site.unregister(Movie)  # unregister first to avoid a conflict
admin.site.register(Movie, MovieAdmin)
