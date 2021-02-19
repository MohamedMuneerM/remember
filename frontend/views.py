from django.shortcuts import render
from .forms import DateForm


def dashboard(request, *args, **kwargs):
	return render(request, 'frontend/pages/dashboard/dashboard.html',{"dateform":DateForm})

# def login(request, *args, **kwargs):
# 	return render(request, 'frontend/pages/auth/login.html',{})


# def register(request, *args, **kwargs):
# 	return render(request, 'frontend/pages/auth/register.html',{})


def landing(request, *args, **kwargs):
	return render(request, 'frontend/pages/landing.html',{})

