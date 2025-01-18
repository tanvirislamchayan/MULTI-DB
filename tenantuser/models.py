from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Subadmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_subadmin = models.BooleanField(default=False)