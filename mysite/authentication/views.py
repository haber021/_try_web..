from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import EmailMessage
import smtplib
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from .utils import token_generator
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error':'email is ivalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email in use chooce another one'}, status=409)
        return JsonResponse({'email_valid': True})



class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain aphanumeric character'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry uusername is use, chooce another one'}, status=409)

        return JsonResponse({'username_valid': True})




    
class SignupView(View):
    def get(self, request):
        return render(request, 'authentication/signup.html')

class ProfileView(View):
    def get(self, request):
        return render(request, 'authentication/profile.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):

        messages.success(request,'Success the whatsapp success')
        messages.warning(request,'Success the whatsapp warning')
        messages.info(request,'Success the whatsapp info')
        messages.error(request,'Success the whatsapp error')

        return render(request, 'authentication/register.html')
    


# email verifacation
class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {'fieldValues': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                connection.starttls()
                connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                token = token_generator.make_token(user)
                link = reverse('authentication:activate', kwargs={'uidb64': uidb64, 'token': token})
                activate_url = 'http://' + domain + link
                
                email_subject = 'Activate your account'
                email_body = f'Hi {user.username}, please use this link to verify your account: {activate_url}'
                send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email])

                connection.quit()

                messages.success(request, 'Account successfully created. Please check your email to activate your account.')
                return render(request, 'authentication/register.html')

        messages.error(request, 'Username or email already exists')
        return render(request, 'authentication/register.html', context)

#
class VerificationView(View):
    def get(self, request, uidb64, token):
        #active user
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('authentication:register'+'?message='+'User already activited')

            if user.is_active:
                return redirect('authentication:register')
            user.is_active = True
            user.save()

            messages.success(request,'Account activited successfully')
            return redirect('authentication:register')

        except Exception as e:
            pass
            
        return redirect('authentication:register')

# login form


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.username}. You are now logged in.')
                    return redirect('expenses:index')
                else:
                    messages.error(request, 'Your account is not active. Please check your email.')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Please fill in all fields.')

        return render(request, 'authentication/login.html')   


#logout
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect(reverse('authentication:login'))