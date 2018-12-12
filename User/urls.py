from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/',views.logIn),
    path('check/',views.check),
    path('forget/',views.forget),
    path('set/',views.set),
    path('logout/',views.logOut),
    path('reset/',views.reset),
]