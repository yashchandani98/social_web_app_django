from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MyProfileView,ProfileView

# setting app_name as accounts
app_name = 'accounts'
# declaring all the url path for accounts app
urlpatterns = [
    path(
        'register/', #signup url
        RegisterView.as_view(),
        name='accounts-register'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='accounts-login'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='accounts-logout'
    ),
    path(
        'myProfile/',
        MyProfileView.as_view(),
        name='myProfile'
    ),
    path(
        'profile/',
        ProfileView.as_view(),
        name='profile-view'
    )
]