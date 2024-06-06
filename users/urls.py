from django.urls import path

from users.apps import UsersConfig
from users.views import generate_new_password, verification, ProfileUpdateView, UserListView, \
    status_user, RegisterUserView, UserLoginView, UserLogoutView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/generate_new_password/', generate_new_password, name='generate_new_password'),
    path('verification/<str:code>/', verification, name='verification'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('status_user/<int:pk>', status_user, name='status_user'),
]

