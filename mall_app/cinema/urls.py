from django.urls import path, include

from mall_app.cinema.views import CinemaScheduleView

urlpatterns = (
path('', CinemaScheduleView.as_view(), name='cinema_schedule'),

)
