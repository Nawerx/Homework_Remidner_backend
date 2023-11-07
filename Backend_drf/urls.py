import knox.views
from django.urls import path, include, re_path
from .views import UserTasksViewSet, UserViewSet, UserRegisterView, UserLoginView
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

nested_router = routers.NestedSimpleRouter(router, "users", lookup="author")
nested_router.register(r"task", UserTasksViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
    path("signup/", UserRegisterView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("logout/", knox.views.LogoutView.as_view())
]