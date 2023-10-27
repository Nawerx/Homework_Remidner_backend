from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("username is required field")
        if not password:
            raise ValueError("password is required field")

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    username = models.CharField(db_column="username", unique=True, max_length=64)
    date_joined = models.DateTimeField(db_column="date joined", default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()




