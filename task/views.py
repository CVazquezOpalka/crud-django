from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .formulario import CreatedTaskForm
from .models import Task
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            "form": UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Username al ready exists"
                })
        else:
            return render(request, "signup.html", {
                "form": UserCreationForm,
                "error": "Password doest match"
            })

@login_required
def tasks(request):
    print(request.user)
    task = Task.objects.filter(user=request.user, datecomplited__isnull=True)
    return render(request, 'tasks.html', {
        "task": task
    })

@login_required
def task_completed(request):
    task = Task.objects.filter(
        user=request.user, datecomplited__isnull=False).order_by("-datecomplited")
    return render(request, 'tasks.html', {
        "task": task
    })

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id)
        form = CreatedTaskForm(instance=task)
        return render(request, 'task_detail.html', {
            "task": task,
            "form": form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = CreatedTaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                "task": task,
                "form": form,
                "error": "Error updating task"
            })

@login_required
def completed_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecomplited = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('tasks')


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            #
            return render(request, 'signin.html', {
                "form": AuthenticationForm,
                "error": "Usuario no encontrado"
            })
        else:
            #
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            "form": CreatedTaskForm,
            "error": "Algo ah ocurrido intenta de enuevo"
        })
    else:
        try:
            form = CreatedTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                "form": CreatedTaskForm,
                "error": "Please Provide validate data"
            })
