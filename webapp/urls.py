# imports 
from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.home, name="home"),
    path('student_login', views.student_login, name="student_login"),
    path('admin_login', views.admin_login, name="admin_login"),
    path('student_profile', views.student_profile, name="student_profile"),
    path('admin_dashboard', views.admin_dashboard, name="admin_dashboard"),
]
