from django.urls import path
from django.contrib.auth import views as auth_views

from mall_app.users.views import RegisterUserView, LoginUserView, LogoutUserView, index, UserProfileView, \
    UserProfileDeleteView, increase_item_quantity

urlpatterns = (
    path('', index, name='index'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='delete_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user_templates/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user_templates/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_templates/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user_templates/password_reset_complete.html'), name='password_reset_complete'),
    path('increase_item_quantity/', increase_item_quantity, name='increase_item_quantity'),
)
