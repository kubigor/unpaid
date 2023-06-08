from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileChangeForm
from pages.models import Member

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            id=request.user.id
            new_member = Member.objects.create(id=id, first_name=first_name, last_name=last_name, username=username, email=email)
            new_member.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Welcome in!')
    else:
        form = UserRegistrationForm

    return render(request, 'profiles/registration.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in!")
            return render(request, 'profiles/login.html')
        else:
            messages.error(request, "No match!")
            return render(request, 'profiles/login.html')
    
    else:
        return render(request, 'profiles/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out!")
    return redirect('/')

@login_required(login_url='/profile/login')
def profile_update(request):
    current_user = User.objects.get(id=request.user.id)
    form = ProfileChangeForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save()
        messages.success(request, "Changes have been applied!")


    return render(request, 'profiles/profile_update.html', {'form': form})

@login_required(login_url='/profile/login')
def profile(request):
    profile_info = User.objects.get(username=request.user.username)
    return render(request, 'profiles/profile.html', {'profile_info': profile_info})

