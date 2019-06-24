from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from .views import user_login, user_register

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login_form.html'), name="user-login"),
    path('logout/', LogoutView.as_view(template_name="users/logout.html"), name="user-logout"),
    path('register/', user_register, name='user-register')
]