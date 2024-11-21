from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError

class ManagerUser(UserManager):
    def create_user(self, email: str, password: str = None, **extra_fields):
        if not email:
            raise ValidationError("Users must have an email address")

        email = self.normalize_email(email=email)
        extra_fields.setdefault("username", None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    objects = ManagerUser()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
