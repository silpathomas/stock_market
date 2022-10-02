from django.urls import path
from user.views import RegisterView
from . import views as user

urlpatterns = [
    # Your URLs...
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login', user.login_user, name="login"),
    path('logout', user.logout_user, name="logout"),

]
