from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PublicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute = models.CharField(max_length=255, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
