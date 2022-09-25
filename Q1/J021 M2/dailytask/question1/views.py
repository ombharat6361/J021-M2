from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# tasks=[
#     {'id':1,'name':"Do the dishes"},{'id':2,'name':"Do laundry"}
# ]

def home(request):
    #user = User.objects.get(id=pk)
    #tasks=user.task_set.all()
    tasks=Task.objects.all()
    context={'tasks':tasks}
    return render(request,"base/home.html",context)

def userTasks(request,pk):
    task=Task.objects.get(id=pk)
    context={'task':task}
    return render(request,"base/tasks.html",context)

@login_required(login_url='login')
def createTask(request):
    form=TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            # room.host=request.user
            # task.save()
            messages.success(request, 'Task created')
            return redirect('home')
    
    context={'form':form}
    return render(request, 'base/task_form.html',context)
@login_required(login_url='login')
def deleteTask(request,pk):
    task=Task.objects.get(id=pk)
    if request.method=='POST':
        task.delete()
        messages.success(request, 'Task deleted')
    context={"obj":task}
    return render(request, "base/delete.html",context)

@login_required(login_url='login')
def updateTask(request,pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.user!=task.host:
        return HttpResponse("You are not allowed to change this task")

    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('home')

    context={'form':form}
    return render(request, "base/task_form.html",context)

def loginPage(request):

    page = 'login'
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"Username or password is invalid")
        
        user=authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password is invalid')
    
    if request.user.is_authenticated:
        return redirect('home')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')


    context={'form':form}
    return render(request,'base/login_register.html',context)

# def dashboard(request,pk):
#     user = User.objects.get(id=pk)
#     tasks=user.task_set.all()

#     context={'user':user,'tasks':tasks}

#     return render(request,'base/profile.html',context)

