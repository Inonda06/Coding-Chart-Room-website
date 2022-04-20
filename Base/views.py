from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message, Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def LoginPage(request):
    page = 'Login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User or password is not correct")
    context = {}
    return render(request, 'base/login_page.html', context)


def LogOut(request):
    logout(request)
    return redirect('home')


def RegisterPage(request):
    page = 'Register'
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, ("an error occured during registration"))

    context = {'form': form, 'page': page}
    return render(request, 'base/login_page.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics,
               'rooms_count': rooms_count, 'room_messages': room_messages}
    return render(request, 'Base/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants
               }
    return render(request, 'Base/room.html', context)


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'Base/profile.html', context)


@login_required(login_url='login')
def CreateRoom(request):
    topics = Topic.objects.all()

    form = RoomForm()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description= request.POST.get('description'),
        )
        #if form.is_valid():
           # room = form.save(commit=False)
            #room.host = request.user
            #room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics= Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('YOU ARE NOT ALLOWED HERE')
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name= request.POST.get("name")
        room.description= request.POST.get('description')
        room.topic=topic
        room.save
        
        return redirect('home')
    context = {'form': form,'topics':topics,'room':room}
    return render(request, 'Base/room_form.html', context)


@login_required(login_url='login')
def DeleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('YOU ARE NOT ALLOWED HERE')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'message': message}
    return render(request, 'Base/delete.html', context)


@login_required(login_url='login')
def DeleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('YOU ARE NOT ALLOWED HERE')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(request, 'Base/delete.html', context)

@login_required(login_url='login')
def updateuser(request,pk):
    return render(request,'Base/update-user.html')
