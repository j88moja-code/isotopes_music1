from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import uuid
import datetime

class Permission(models.Model):
    name = models.CharField(max_length=100)

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def profile_file_upload_path(instance, filename):
    now = datetime.datetime.now()
    return (
        f"user_{instance.user.id}/"
        f"date_{now.year}_{now.month}_{now.day}/"
        f"time_{now.hour}_{now.minute}_{now.second}/"
        f"{filename}"
    )

class User(AbstractUser):
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4,
        editable = False, 
        unique=True
        )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    dob=models.DateField(null=True,blank=True,default=None)
    phone=models.CharField(max_length=20,null=True,blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_image=models.ImageField(upload_to=profile_file_upload_path,null=True,blank=True, default='blank_profile_image.png')
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
 
class UserFollow(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="src_follow")
    follows = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="dest_follow")

