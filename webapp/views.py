import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase app (ensure the path to your service account key is correct)
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'firebase_key.json'))
firebase_admin.initialize_app(cred)

FIREBASE_API_KEY = "AIzaSyCcG9zS8hJBVQ-c5budSk8QAjSOdMLdJ18"

def home(request):
    return render(request, 'home.html')

def student_login(request):
    return render(request, 'student_login.html')

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('admin_username')
        password = request.POST.get('admin_password')

        # Authenticate with Firebase
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}", data=payload)

        if response.status_code == 200:
            id_token = response.json()['idToken']
            try:
                # Verify the ID token
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']
                # print(uid)

                # You can add additional checks, such as checking for a specific role
                user = auth.get_user(uid)
                # print(user.email)
                if email == user.email:
                    return redirect('admin_dashboard')
                else:
                    return HttpResponse("Unauthorized", status=401)
            
            except auth.InvalidIdTokenError:
                return HttpResponse("Invalid token. Please try again.", status=400)
        
        else:
            return HttpResponse("Authentication failed. Please check your credentials and try again.", status=401)
    
    return render(request, 'administrator_login.html')


def student_profile(request):
    return render(request, 'student_profile.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
