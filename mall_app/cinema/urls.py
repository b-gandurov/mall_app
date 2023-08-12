from django.urls import path
from mall_app.cinema.views import CinemaScheduleView, UnbookSeatView

urlpatterns = (
    path('', CinemaScheduleView.as_view(), name='cinema_schedule'),
    path('unbook_seat/<int:ticket_id>/', UnbookSeatView.as_view(), name='unbook_seat'),

)
