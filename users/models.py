from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, profile_picture=None, is_superadmin=False, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            profile_picture=profile_picture,
            is_superadmin=is_superadmin,
            is_staff=is_staff,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        # Assign user to appropriate group
        if is_superadmin:
            group = Group.objects.get(name='superadmin')
            user.groups.add(group)
        elif is_superuser:
            group = Group.objects.get(name='superuser')
            user.groups.add(group)
        else:
            group = Group.objects.get(name='user')
            user.groups.add(group)
        return user

    def create_superuser(self, email, full_name, password=None, profile_picture=None):
        user = self.create_user(
            email,
            full_name,
            password,
            profile_picture,
            is_staff=True,
            is_superuser=True,
        )
        # Add to superadmin group
        group = Group.objects.get(name='superadmin')
        user.groups.add(group)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
