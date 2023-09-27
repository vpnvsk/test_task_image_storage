from django.db import models
from django.contrib.auth.models import AbstractUser


class Thumbnail(models.Model):
    size = models.IntegerField(unique=True)

    class Meta:
        verbose_name = "Thumbnail"
        verbose_name_plural = "Thumbnails"


class Tier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail_size = models.ManyToManyField(Thumbnail)
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tier"
        verbose_name_plural = "Tiers"


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    password = models.CharField()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
