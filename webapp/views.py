from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')

def student_login(request):
    return render(request, 'student_login.html')

def admin_login(request):
    return render(request, 'admin_login.html')

def student_profile(request):
    return render(request, 'student_profile.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
