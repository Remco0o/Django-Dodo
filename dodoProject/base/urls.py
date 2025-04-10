from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("logout_user/", views.logout_user, name="logout_user"),
    path("unapproved_dead/", views.unapproved_dead, name="unapproved_dead"),
    path("approve_dead/<int:pk>/", views.approve_dead, name="approve_dead"),
    path("deny_dead/<int:pk>/", views.deny_dead, name="deny_dead"),
    path("add_dodo/", views.add_dodo, name="add_dodo"),
]
