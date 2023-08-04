from django.urls import path

from mall_app.users.views import RegisterUserView, LoginUserView, LogoutUserView, index, UserProfileView, \
    UserProfileDeleteView

urlpatterns = (
    path('', index, name='index'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='delete_profile'),
)
