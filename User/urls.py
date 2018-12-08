from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/',views.logIn),
    path('check/',views.check),
]