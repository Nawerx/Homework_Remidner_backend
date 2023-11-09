from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import login
from .serializers import UserSerializer, SimpleTaskSerializer, RegisterSerializer, AuthTokenSerializer
from .models import User, Task
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from knox.auth import AuthToken
# Create your views here.


class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format="email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            201: 'Created',
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            data = {"user": serializer.data,
                    "token": token}

            if user:
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format="email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            }
        ),
        responses={
            200: 'OK',
            400: 'Bad Request',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

            _, token = AuthToken.objects.create(user)

            return Response({"user_info": {
                                            "id": user.id,
                                            "email": user.email
                                          },
                            "token": token
            }
            )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserTasksViewSet(ModelViewSet):
    serializer_class = SimpleTaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs["author_pk"]
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author_id=author_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_queryset(self):
        author_id = self.kwargs["author_pk"]
        return Task.objects.filter(author_id=author_id)


