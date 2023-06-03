from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm 
from .models import Post
from .forms import PostForm

def create_post(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/newpost?submitted')
    else:
        form = PostForm
        if 'submitted' in request.GET:
            submitted = True
        
    return render(request, 'pages/newpost.html', {'form':form, 'submitted': submitted})

def header(request):
    return render(request, 'pages/header.html')

def posts(request):
    return render(request, 'pages/posts.html')