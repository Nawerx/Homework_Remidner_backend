from django.urls import path

from .views import UserLoginView, UserRegisterView

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("signup/", UserRegisterView.as_view()),
]