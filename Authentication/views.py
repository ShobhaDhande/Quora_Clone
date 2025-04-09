from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View



class LoginView(View):
    """
    Handles user login functionality.

    GET: Renders the login form.
    POST: Authenticates and logs in the user using email and password.
    """

    def get(self, request):
        # Render the login form
        return render(request, 'login.html')

    def post(self, request):
        try:
            # Get email and password from POST request
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(email, password)  # Debugging print (can remove)

            # Authenticate using email (custom authentication backend should be set up)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Login the user and redirect to dashboard
                login(request, user)
                return redirect('dashboard')
            else:
                # Invalid credentials
                return HttpResponse('Invalid username or password', status=401)

        except Exception as e:
            return HttpResponse('An error occurred during login', status=500)


class SignupView(View):
    """
    Handles user signup functionality.

    GET: Renders the signup form.
    POST: Registers a new user after validating form data.
    """

    def get(self, request):
        # Render the signup form
        return render(request, 'signup.html')

    def post(self, request):
        try:
            # Extract user input from POST data
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirm = request.POST.get('confirm_password')

            # Validate password confirmation
            if password != password_confirm:
                return HttpResponse('Passwords do not match', status=400)

            # Check for existing email
            if User.objects.filter(email=email).exists():
                return HttpResponse('Email already taken', status=400)

            # Check for existing username
            if User.objects.filter(username=username).exists():
                return HttpResponse('Username already taken', status=400)

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Authenticate and login the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')

            return HttpResponse('Something went wrong', status=500)

        except Exception as e:
            return HttpResponse('An error occurred during signup', status=500)


class LogOutView(LoginRequiredMixin,View):
    """
    Handles user logout functionality.

    GET: Logs out the current user and redirects to the homepage.
    """

    def get(self, request):
        try:
            # Log out the user
            logout(request)
            return redirect('/')
        except Exception as e:
            return HttpResponse('An error occurred during logout', status=500)
