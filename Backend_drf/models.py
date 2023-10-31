from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("username is required field")
        if not password:
            raise ValueError("password is required field")


        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    email = models.EmailField("email address", max_length=264, unique=True)
    password = models.CharField("password", max_length=264)
    first_name = models.CharField("first name", max_length=64, null=False)
    last_name = models.CharField("last name", max_length=64, null=False)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password", "first_name", "last_name"]

    objects = CustomUserManager()


class Task(models.Model):
    id = models.AutoField(primary_key=True)

    subject = models.CharField("subject", max_length=64, null=False)
    deadline = models.DateField("deadline", null=False)
    task = models.TextField("task", max_length=264)
    details = models.TextField("details", max_length=264)
    is_done = models.BooleanField("is_active", default=False)

    author = models.ForeignKey(User, db_column="author_id", on_delete=models.CASCADE, related_name="posts")




