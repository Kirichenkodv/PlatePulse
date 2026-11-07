from django.db import models

from config import settings


class HouseHold(models.Model):
    name = models.CharField(verbose_name="Название семьи", unique=True)
    created_at = models.DateTimeField(verbose_name="время создания семьи")

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Семья"
        verbose_name_plural = "Семьи"


class HouseHoldInvite(models.Model):
    household = models.ForeignKey(
        HouseHold,
        on_delete=models.CASCADE,
        related_name="invites",
        verbose_name="Приглашение",
    )
    email = models.EmailField()
    invite_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_household_invite",
    )
    token_hash = models.CharField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(
        verbose_name="Срок действия",
        null=True,
        blank=True,
    )
    revoke_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Когда отменили",
    )
