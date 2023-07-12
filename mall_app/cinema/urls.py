from django.urls import path, include

# from mall_app.cinema.models import BookSeatsView
from mall_app.cinema.views import CinemaScheduleView

urlpatterns = (
path('', CinemaScheduleView.as_view(), name='cinema_schedule'),
# path('book_seats/', BookSeatsView.as_view(), name='book_seats'),

)
