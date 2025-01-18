from django.test import TestCase
from .models import Client, Domain
from decouple import config

# Create your tests here.

def create():
    default_schema = config('DEFAULT_SCHEMA')
    default_schema_name = config('DEFAULT_SCHEMA_NAME')
    default_domain = config('DEFAULT_DOMAIN')

    tenant = Client(schema_name=default_schema, name=default_schema_name)
    tenant.save()

    domain = Domain(domain=default_domain, tenant=tenant, is_primary=True)
    domain.save()

    return{
        'tenant': tenant,
        'domain': domain,
    }

