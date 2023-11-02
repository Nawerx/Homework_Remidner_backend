from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Task


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


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        user = authenticate(
            email=validated_data["email"], password=validated_data["password"]
        )
        if not user:
            raise serializers.ValidationError("User not found")
        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"], password=validated_data["password"],
                                        first_name=validated_data["first_name"], last_name=validated_data["last_name"])

        return user