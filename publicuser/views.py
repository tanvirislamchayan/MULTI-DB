from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django_tenants.utils import schema_context
from public.models import Domain, Client
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import PublicUser
from .default import create_superuser, create_subadmin
# Create your views here.


def user_login(request):
    current_schema = request.tenant.schema_name
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not all([username, password]):
            messages.warning(request, 'Usernme and Password both are required.')
            return HttpResponseRedirect(referal_url)
        with schema_context(current_schema):
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                login(request, user)
                print('success')
                messages.success(request, 'Login successfull.')
                return redirect('public_home')
            else:
                messages.error(request, 'Invalid Username or Password. Please check and try again.')
                return HttpResponseRedirect(referal_url)
    return render(request, 'public/public_user_login.html')

def user_register(request):
    current_schema = request.tenant.schema_name
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        institute = request.POST.get('institute', '')
        password = request.POST.get('password', '')
        con_pass = request.POST.get('con_pass', '')
        if not password == con_pass:
            messages.warning(request, "Password doesn't match.")
            return HttpResponseRedirect(referal_url)
        
        with schema_context(current_schema):
            try:
                user, created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                    }
                )
                if created:
                    user.set_password(password)
                    user.save()
                    public_user, created_public = PublicUser.objects.get_or_create(
                        user=user,
                        defaults={
                            'phone': phone,
                            'institute': institute,
                        }
                    )
                    if created_public:
                        messages.success(request, 'Registration Successfull')
                        return redirect('public_user_login')
                    else:
                        messages.error(request, 'Something went Wrong!')
                        return HttpResponseRedirect(referal_url)
                else:
                    messages.error(request, 'User already exists. Please Login.')
                    return redirect('public_user_login')
            except Exception as e:
                print(e)
    return render(request, 'public/public_user_register_form.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout Successfull.')
    return redirect('public_home')


def book(request):
    publicuser_obj = PublicUser.objects.get(user=request.user)
    publicuser_institute = publicuser_obj.institute
    context = {
        'institute': publicuser_institute if publicuser_institute else False
    }

    # Get the domains from the current schema
    domains = []
    current_schema = request.tenant.schema_name
    referal_url = request.META.get('HTTP_REFERER', request.path_info)
    with schema_context(current_schema):
        domain_objs = Domain.objects.all()
        for domain in domain_objs:
            if len(domain.domain.split('.')) >=2:
                domains.append(domain.domain.split('.')[1])
                print(domain.domain.split('.'))
            # domains.append(domain.domain.split('.'))  # Extract the subdomain part before the dot

    if domains:
        context.update({
            'domains': domains
        })

    if request.method == 'POST':
        print("POST method received")  # Add a print to check if POST is being received
        institute = request.POST.get('institute', '')
        fix_domain = request.POST.get('fix_domain', '')
        sub_domain = request.POST.get('sub_domain', '')
        main_domain = request.POST.get('main_domain', '')
        password = request.POST.get('password')
        con_pass = request.POST.get('con_pass')
        if not password == con_pass:
            messages.warning(request, "Password Doesn't match")
            return HttpResponseRedirect(referal_url)
        schema_name = '_'.join(institute.lower().split())
        domain_name = f'{fix_domain}.{sub_domain}.{main_domain}'

        if not all([institute, fix_domain, sub_domain, main_domain]):
            messages.error(request, 'All the fields are rquired')
            return HttpResponseRedirect(referal_url)
        
        try:
            with schema_context(current_schema):
                tenant, created = Client.objects.get_or_create(
                    schema_name = schema_name,
                    defaults={
                        'name': institute
                    }
                )
                if created:
                    messages.success(request, 'Schema created successfully.')
                    domain_obj, domain_created = Domain.objects.get_or_create(
                        domain = domain_name,
                        defaults={
                            'is_primary':True,
                            'tenant':tenant
                        }
                    )
                    if domain_created:
                        messages.success(request, f'Domain created {domain_obj.domain}')
                        create_superuser(schema_name)
                        create_subadmin(schema_name, request.user, password)
                        return HttpResponseRedirect(referal_url)
                        
                    else:
                        tenant.delete()
                        messages.warning(request, 'Domain already exists')
                        messages.warning(request, 'Schema Deleted')
                        return HttpResponseRedirect(referal_url)
                else:
                    messages.error(request, 'Schema already Exists.')
                    return HttpResponseRedirect(referal_url)
            
        except Exception as e:
            print(e)


    return render(request, 'public/book_software.html', context)

