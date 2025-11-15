# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

def home(request):
    # simple home page that links to login/signup
    return render(request, "accounts/home.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on role
            if user.role == "patient":
                return redirect("patient_dashboard")
            elif user.role == "doctor":
                return redirect("doctor_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("home")

@login_required
def patient_dashboard(request):
    # ensure only patient users access (optional)
    if request.user.role != "patient":
        messages.error(request, "You are not authorized to view this page.")
        return redirect("home")
    return render(request, "accounts/patient_dashboard.html")

@login_required
def doctor_dashboard(request):
    if request.user.role != "doctor":
        messages.error(request, "You are not authorized to view this page.")
        return redirect("home")
    return render(request, "accounts/doctor_dashboard.html")
