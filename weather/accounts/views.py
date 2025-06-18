from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Profile

def login_view(request):
    """Authenticate and log in a user.
    On successful login, redirect to the home dashboard."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def dashboard(request):
    """Render the user dashboard/homepage.
    This page serves as the landing view after login."""
    return render(request, 'accounts/home.html')

def register(request):
    """Register a new user account.
    Creates user, profile, logs them in, and redirects to home."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated profile
            Profile.objects.create(user=user)
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"Welcome {username}! Your account has been created successfully.")
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    """Log out the current user.
    Redirect to the home page with a success message."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')
