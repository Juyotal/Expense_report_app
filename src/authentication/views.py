from django import contrib
import django
from django.shortcuts import redirect, render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.contrib import auth, messages
from validate_email import validate_email
from django.core.mail import EmailMessage



# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username already being used. please choose another'}, status=409)

        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email you Entered is invalid'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry Email already has an account'}, status=409)

        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active= True
                user.save()
                # email_subject = 'Activate email accont'
                # email_body = 'Tesst body'
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@emaol.com',
                #     [email],
                # )

                # email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')

                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')



class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
    
        if username and password:

            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in.')
                    return redirect('expenses')

                else:
                    messages.error(request, 'Account is not active, please reactivate')
                    return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, please try again')
            return render(request, 'authentication/login.html' )

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

# @csrf_protect
class LogoutView(View):

    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been Logged Out')
        return redirect('login')
