from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.dispatch import receiver
from django.core.signals import request_started, request_finished
from django.contrib.sessions.backends.db import SessionStore
from firebase_admin import credentials, auth, db

import requests
import firebase_admin
import pandas as pd
import os

# Initialize Firebase app (ensure the path to your service account key is correct)
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), './static/extras/firebase_key.json'))
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://placement-web-portal-c3159-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

FIREBASE_API_KEY = "AIzaSyCcG9zS8hJBVQ-c5budSk8QAjSOdMLdJ18"


def home(request):
    request.session["home_visited"] = True
    request.session["is_authenticated"] = False
    years = fetch_years()
    year = max(years)
    context = fetch_data(year)
    context["selected_year"] = year
    return render(request, 'home.html', context)


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

                # You can add additional checks, such as checking for a specific role
                user = auth.get_user(uid)
                if email == user.email:
                    # Store authentication status in session
                    request.session['is_authenticated'] = True
                    return redirect('admin_dashboard')
                else:
                    error_message = "Invalid credentials. Please try again."
                    return render(request, 'administrator_login.html', {'error_message': error_message})
            
            except auth.InvalidIdTokenError:
                error_message = "Invalid token. Please try again."
                return render(request, 'administrator_login.html', {'error_message': error_message})
        
        else:
            error_message = "Authentication failed. Please check your credentials and try again."
            return render(request, 'administrator_login.html', {'error_message': error_message})
    
    return render(request, 'administrator_login.html')


def student_profile(request):
    return render(request, 'student_profile.html')


def admin_dashboard(request):
    if not request.session.get('is_authenticated', False):
        return redirect('admin_login')
    try:
        if not request.session.get('home_visited'):
            return redirect('admin_login')
    except Exception as e:
            return redirect('admin_login')

    selected_year = request.POST.get('year') if request.method == "POST" else '2024'
    context = fetch_data(selected_year)
    context['selected_year'] = selected_year
    context['years_list'] = fetch_years()

    return render(request, 'admin_dashboard.html', context)

    try:
        if not request.session.get('is_authenticated', False):
            return redirect('admin_login')  # Redirect to login page if not authenticated
        if not(request.session.get('home_visited')):
            raise Exception
    except Exception as e:
            return redirect('admin_login')  # Redirect to login page if not authenticated

    if request.method == "POST":
        selected_year = request.POST.get('year')
        context = fetch_data(selected_year)
        context['selected_year'] = selected_year
    else:
        # If the request method is GET, default to the current year
        selected_year = '2024'  # Change this to your default year
        context = fetch_data(selected_year)
        context['selected_year'] = selected_year

    context['years_list'] = fetch_years()

    return render(request, 'admin_dashboard.html', context)


def fetch_data(year):
    # Fetch data from Firebase
    result = db.reference(f'/batches/{year}').get()

    # Convert Firebase data to pandas DataFrame
    df = pd.DataFrame(result)

    # Calculate average and highest CTC
    avg_ctc = df['CTC'].mean()
    highest_ctc = df['CTC'].max()

    # Generate pie chart data
    dream_ctc = ((df['CTC'] >= 500000) & (df['CTC'] <= 1000000)).sum()
    super_dream_ctc = ((df['CTC'] > 1000000) & (df['CTC'] <= 2000000)).sum()
    marquee_ctc = (df['CTC'] > 2000000).sum()
    pie_chart_data = [dream_ctc, super_dream_ctc, marquee_ctc]

    # Filter top recruiters
    top_recruiters_count = df['Final Offer'].value_counts().to_dict()
    top_recruiters_lst= [key for key in top_recruiters_count if top_recruiters_count[key] > 10]
    avg_floored_ctc = avg_ctc//100000

    context = {
        'highest_ctc': highest_ctc,
        'avg_floored_ctc': avg_floored_ctc,
        'pie_chart_data': pie_chart_data,
        'top_recruiters_lst': top_recruiters_lst
    }

    return context


def fetch_years():
    years_lst = list(db.reference('/years').get())
    return years_lst

