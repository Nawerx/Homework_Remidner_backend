from django.urls import path, include
from .views import UserLoginView, UserRegisterView, UserTasksViewSet, UserViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

nested_router = routers.NestedSimpleRouter(router, "users", lookup="author")
nested_router.register(r"task", UserTasksViewSet, basename="task")

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("signup/", UserRegisterView.as_view()),
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
]