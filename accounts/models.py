import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.PositiveSmallIntegerField(default=18)
    fullname = models.CharField(max_length=100, default='')
    role = models.CharField(max_length=100, default='user')
    avatar = models.CharField(max_length=100, default='https://www.gravatar.com/avatar/?d=mp')
    is_verified = models.BooleanField(default=False)
    is_gplx = models.BooleanField(default=False)
    is_bhyt=models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Notification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    type = models.CharField(max_length=10, default='')
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="notifications",
        default=1
    )

