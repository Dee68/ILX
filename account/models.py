from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin
                                        )
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username!')
        if email is None:
            raise TypeError('User should have an Email')
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        if password is None:
            raise TypeError('Superuser should have a password!')
        # user.is_superuser = True
        # user.is_active = True
        # user.is_staff = True
        user = self.create_user(username, email, password, **extra_fields)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=60,
        db_index=True
        )
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password1 = models.CharField(max_length=20, default='password')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
        return self.username


class Profile(models.Model):
    """User profile to extend the account profile
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default='firstname')
    last_name = models.CharField(max_length=20, default='lastname')
    street_address1 = models.CharField(blank=True, max_length=100, null=True)
    town_or_city = models.CharField(blank=True, max_length=30)
    county = models.CharField(blank=True, default=00, max_length=30, null=True)
    postcode = models.CharField(blank=True, max_length=30)
    avatar = models.ImageField(blank=True, upload_to='profile_pics/')

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<img src="%s" height="50" width="50">' % self.avatar.url
                )
        return "No image found"
    
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)