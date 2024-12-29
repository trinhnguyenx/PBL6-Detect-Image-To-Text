from django.db import models
from accounts.models import CustomUser
import uuid


class CommonCard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=255, null=True, blank=True)
    expire_date = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    images = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - {self.type}"


class CCCDCard(CommonCard):
    gender = models.CharField(max_length=255, null=True, blank=True)
    origin_place = models.CharField(max_length=255, null=True, blank=True)
    current_place = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    personal_identifi = models.CharField(max_length=255, null=True, blank=True)
    images_behind = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cccd_cards",
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'id'], name='unique_user_cccd_card')
        ]


class GPLXCard(CommonCard):
    level = models.CharField(max_length=255, null=True, blank=True)
    iplace = models.CharField(max_length=255, null=True, blank=True)
    origin_place = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="gplx_cards",
        default=1

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'id'], name='unique_user_gplx_card')
        ]


class BHYTCard(CommonCard):
    ihos = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    iplace = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="bhyt_cards",
        default=1
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'id'], name='unique_user_bhyt_card')
        ]
