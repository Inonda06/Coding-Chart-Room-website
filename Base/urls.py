from django.urls import path
from .import views

urlpatterns=[
    path("Login/", views.LoginPage, name='login'),
    path("LogOut/", views.LogOut, name='logout'),
    path("Register/", views.RegisterPage, name='Register'), 
    path("", views.home, name='home'),
    path('room/<str:pk>/',views.room, name='room'),
    path("profile/<str:pk>/", views.UserProfile, name='profile'),
    path("Create-Room/",views.CreateRoom, name= 'CreateRoom'),
    path("UpdateRoom/<str:pk>/", views.UpdateRoom, name= 'RoomUpdate'),
    path("Delete-Room/<str:pk>/", views.DeleteRoom, name='DeleteRoom'),
    path("Delete-message/<str:pk>/", views.DeleteMessage, name='delete-message'),
     path("update-user/<str:pk>/", views.updateuser, name='updateuser'),


]