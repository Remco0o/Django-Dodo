from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Dodo, Update
from .forms import DodoForm, ProfileForm, UpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


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


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@staff_member_required
def unapproved_dead(request):
    dodos = Dodo.objects.filter(dead_approved=False, alive=False)
    context = {'dodos': dodos}
    return render(request, 'base/unapproved_dead.html', context)


@staff_member_required
def approve_dead(request, pk):
    dodo = Dodo.objects.get(pk=pk)
    dodo.dead_approved = True
    dodo.dead_approved_by = request.user
    dodo.save()
    messages.success(request, "Dead approved")
    return redirect("unapproved_dead")


@staff_member_required
def deny_dead(request, pk):
    dodo = Dodo.objects.get(pk=pk)
    dodo.alive = True
    dodo.save()
    messages.success(request, "Dead denied")
    return redirect("unapproved_dead")


@staff_member_required
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


@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect("index")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "base/edit_profile.html", {"form": form})


@login_required
def add_update(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            dodo = form.cleaned_data['dodo']

            if not dodo.is_alive:
                messages.error(
                    request, "Dodo already dead.")
                return redirect("my_updates")

            update = form.save(commit=False)
            update.user = request.user
            update.save()
            messages.success(request, "Updated!")
            return redirect("newsfeed")
    else:
        form = UpdateForm()

    return render(request, "base/add_update.html", {"form": form})


@login_required
def report_dead(request, pk):
    dodo = Dodo.objects.get(pk=pk)

    if dodo.alive:
        dodo.alive = False
        dodo.dead_approved = False
        dodo.save()

        Update.objects.create(
            dodo=dodo,
            user=request.user,
            description=f"{dodo.name} is reported as dead.",
            date=timezone.now()
        )

        messages.success(request, f"Dodo {dodo.name} dead reported.")
    else:
        messages.info(request, f"Dodo {dodo.name} is already dead.")

    return render(request, 'base/report_dead.html', {'dodo': dodo})


@login_required
def newsfeed(request):
    updates = Update.objects.all().order_by("-date")
    return render(request, "base/newsfeed.html", {"updates": updates})


@login_required
def my_updates(request):
    updates = Update.objects.filter(user=request.user).order_by("-date")
    return render(request, "base/my_updates.html", {"updates": updates})


@login_required
def edit_update(request, pk):
    update = Update.objects.get(pk=pk)
    if update.user != request.user:
        return redirect("my_updates")

    if request.method == "POST":
        form = UpdateForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated!")
            return redirect("my_updates")
    else:
        form = UpdateForm(instance=update)
    return render(request, "base/edit_update.html", {"form": form})


@login_required
def delete_update(request, pk):
    update = Update.objects.get(pk=pk)
    if update.user == request.user:
        update.delete()
        messages.success(request, "Update deleted.")
    return redirect("my_updates")
