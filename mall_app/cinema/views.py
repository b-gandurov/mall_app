from django.db.models import Prefetch
from django.views.generic import ListView
from mall_app.cinema.models import Schedule, Movie


class CinemaScheduleView(ListView):
    model = Movie
    template_name = 'schedule.html'
    context_object_name = 'movies'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related(
            Prefetch('schedule_set', queryset=Schedule.objects.order_by('show_time'))
        )
        return queryset
