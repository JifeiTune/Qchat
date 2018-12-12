from django.urls import path
from . import views

urlpatterns = [
    #主页
    path('', views.all),
    #单个帖子
    path('<int:id>/', views.one),
    path('new/',views.creat),
]