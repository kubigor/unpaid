from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# def login_user(request):
#     return render(request, 'profiles/login.html')
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Success")
            return render(request, 'profiles/login.html')
        else:
            messages.success(request, ("Error"))
            return render(request, 'profiles/login.html')
    
    else:
        return render(request, 'profiles/login.html')

def profile(request):
    return render(request, 'profiles/profile.html')

