from django.urls import path, include

# from mall_app.cinema.models import BookSeatsView
from mall_app.cinema.views import CinemaScheduleView, UnbookSeatView

urlpatterns = (
path('', CinemaScheduleView.as_view(), name='cinema_schedule'),
path('unbook_seat/<int:ticket_id>/', UnbookSeatView.as_view(), name='unbook_seat'),
# path('book_seats/', BookSeatsView.as_view(), name='book_seats'),

)
