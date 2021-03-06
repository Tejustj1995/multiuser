from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("users must have mail")

        user_obj = self.mode(email=self.normalize_email(email))

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.admin = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, is_admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, default='abc')
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
