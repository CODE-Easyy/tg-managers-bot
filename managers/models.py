import datetime
import secrets

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.db import models

def get_new_token():
    return secrets.token_urlsafe(16)


class ManagerManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('User must have email!')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Manager(AbstractBaseUser, PermissionsMixin):
    token = models.CharField(
        max_length=255,
        unique=True,
    )

    name = models.CharField(
        max_length=255,
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
    )


    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'name',
    )

    objects = ManagerManager()


    def set_token(self):
        self.token = get_new_token()
        self.save()

    def save(self, *args, **kwargs): 
        if not (self.token and len(self.token) > 0):
            self.set_token()
        super(Manager, self).save(*args, **kwargs) 


    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return f'Manager("{self.name}")'

    class Meta:
        ordering = ('name',)