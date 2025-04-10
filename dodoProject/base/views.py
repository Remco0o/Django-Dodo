from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Dodo
from .forms import DodoForm
from django.contrib import messages


def index(request):
    return render(request, "base/index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "registration/register.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


def unapproved_dead(request):
    dodos = Dodo.objects.filter(dead_approved=False, alive=False)
    context = {'dodos': dodos}
    return render(request, 'base/unapproved_dead.html', context)


def approve_dead(request, pk):
    dodo = Dodo.objects.get(pk=pk)
    dodo.dead_approved = True
    dodo.dead_approved_by = request.user
    dodo.save()
    messages.success(request, "Dead approved")
    return redirect("unapproved_dead")


def deny_dead(request, pk):
    dodo = Dodo.objects.get(pk=pk)
    dodo.alive = True
    dodo.save()
    messages.success(request, "Dead denied")
    return redirect("unapproved_dead")


def add_dodo(request):
    if request.method == "POST":
        form = DodoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Dodo succesfully added!")
            return redirect("index")
    else:
        form = DodoForm()

    context = {"form": form}
    return render(request, "base/dodoadd.html", context)
