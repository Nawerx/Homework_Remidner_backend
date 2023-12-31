from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED
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

from knox.auth import AuthToken, TokenAuthentication
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

            return Response({"user": {
                                            "id": user.id,
                                            "email": user.email,
                                            "first_name": user.first_name,
                                            "last_name": user.last_name,
                                          },
                            "token": token
            }
            )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from knox.models import AuthToken


class UserTasksViewSet(ModelViewSet):
    serializer_class = SimpleTaskSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        author_id = self.kwargs["author_pk"]

        token = request.META.get('HTTP_AUTHORIZATION').split()[1][:8]

        user_tokens = AuthToken.objects.filter(user_id=author_id).values_list('token_key', flat=True)

        if token in user_tokens:
            queryset = Task.objects.filter(author_id=author_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Access denied: Token does not belong to this user"},
                            status=HTTP_401_UNAUTHORIZED)

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


