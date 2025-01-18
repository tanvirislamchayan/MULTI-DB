from django.db import models
from django_tenants.models import DomainMixin, TenantMixin

# Create your models here.

class Client(TenantMixin):
    name = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass
