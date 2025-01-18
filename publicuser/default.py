from public.models import Client, Domain
from decouple import config
from django.contrib.auth.models import User
from django_tenants.utils import schema_context
from tenantuser.models import Subadmin
from . models import PublicUser


def create_superuser(schema_name):
    superusers = {
        'user_1': {
            'first_name': 'Tanvir',
            'last_name': 'Islam',
            'email': 'imdtanvir181@gmail.com',
            'username': 'imdtanvir181@gmail.com',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'password': '06jstechnology013taNvir49@#',
        },
        'user_2': {
            'first_name': 'Manik',
            'last_name': 'Ullah',
            'email': 'engmanik11@gmail.com',
            'username': 'engmanik11@gmail.com',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'password': '06jstechNology013manikullah49@#',
        },
    }

    for user_name, user_info in superusers.items():
        try:
            with schema_context(schema_name):
                userobj, created = User.objects.get_or_create(
                    username=user_info.get('username', ''),
                    defaults={
                        'first_name': user_info.get('first_name', ''),
                        'last_name': user_info.get('last_name', ''),
                        'email': user_info.get('email', ''),
                        'is_superuser': user_info.get('is_superuser', ''),
                        'is_staff': user_info.get('is_staff', ''),
                        'is_active': user_info.get('is_active', ''),
                    }
                )
                if created:
                    userobj.set_password(config('SUPER_USER_PASSWORD'))
                    userobj.save()
                    print(f'created: {userobj.first_name} {userobj.last_name} - {created}')
                else:
                    userobj.is_staff=user_info.get('is_staff', '')
                    userobj.is_superuser=user_info.get('is_superuser', '')
                    userobj.is_active=user_info.get('is_active', '')
                    userobj.save()
                    
                    print(f'exists update: {userobj.first_name} {userobj.last_name} - {created}')
        except Exception as e:
            print(e)



def create_subadmin(schema_name, user, password):
    try:
        with schema_context(schema_name):
            user_obj, created = User.objects.get_or_create(
                username=user.username,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'last_name': user.last_name,
                    'is_active': user.is_active,
                }
            )
            if created:
                user_obj.set_password(password)
                user_obj.save()
                public_user = PublicUser.objects.get(user=user)
                Subadmin.objects.create(
                    user=user_obj,
                    phone_number=public_user.phone,
                    is_subadmin=True
                )
    except Exception as e:
        print(e)