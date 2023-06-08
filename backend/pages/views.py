from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post, Member

def create_post(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            print(request.user.username)
            print(Member.objects.all())


            obj.author = Member.objects.get(username=request.user.username).id
            obj.save()
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