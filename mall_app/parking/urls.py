from django.urls import path
from mall_app.parking.views import ParkingView, RegisterCarView, CarEntryView, CarExitView, DeleteCarView

urlpatterns = (
    path('', ParkingView.as_view(), name='parking'),
    path('delete_car/<int:pk>/', DeleteCarView.as_view(), name='delete_car'),
    path('register_car/', RegisterCarView.as_view(), name='register_car'),
    path('enter/', CarEntryView.as_view(), name='enter_car'),
    path('exit/', CarExitView.as_view(), name='exit-parking'),
)
