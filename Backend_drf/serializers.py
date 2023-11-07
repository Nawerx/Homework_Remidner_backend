from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Task
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class SimpleTaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')

    class Meta:
        model = Task
        fields = ["id", "subject", "deadline", "task", "details", "is_done"]
        read_only_fields = ["id"]


class UserSerializer(serializers.ModelSerializer):
    tasks = SimpleTaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "tasks"]
        read_only_fields = ["id"]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"], password=validated_data["password"],
                                        first_name=validated_data["first_name"], last_name=validated_data["last_name"])

        return user