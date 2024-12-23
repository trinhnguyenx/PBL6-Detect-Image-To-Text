from django.db import models
from accounts.models import CustomUser
import uuid


class CommonCard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    dob = models.CharField(max_length=255)
    expire_date = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} - {self.type}"


class CCCDCard(CommonCard):
    gender = models.CharField(max_length=255)
    origin_place = models.CharField(max_length=255)
    current_place = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
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
    level = models.CharField(max_length=255)
    iplace = models.CharField(max_length=255)
    origin_place = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
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
    ihos = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    iplace = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=255)
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
