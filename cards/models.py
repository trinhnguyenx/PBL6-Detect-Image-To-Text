from django.db import models
from accounts.models import CustomUser
import uuid

class CCCDCard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    dateOfBirth = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    placeOfOrigin = models.CharField(max_length=255)
    placeOfResidence = models.CharField(max_length=255)
    dateOfExpiry = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cccdCards', default=2)

    def __str__(self):
        return self.fullname
