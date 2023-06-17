from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import PostForm, InquiryForm
from .models import Post, Member, Inquiry, Company, Comment

def create_post(request):
    submitted = False
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = Member.objects.get(username=request.user.username)
            obj.save()
            return HttpResponseRedirect('/newpost?submitted')
    else:
        form = PostForm()
        if 'submitted' in request.GET:
            submitted = True
        
    return render(request, 'pages/newpost.html', {'form':form, 'submitted': submitted})

def create_inquiry(request):
    submitted = False
    if request.method == "POST":
        form = InquiryForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = Member.objects.get(username=request.user.username)
            obj.save()
            return HttpResponseRedirect('/inquiry?submitted')
    else:
        form = InquiryForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'pages/create_inquiry.html', {'form':form, 'submitted': submitted})

def header(request):
    return render(request, 'pages/header.html')

def search(request, table_name, page_number=0):
    print(table_name)
    if table_name == 'inquiries':
        table = Inquiry
    elif table_name == 'companies':
        table = Company
    else: 
        table = Post
    list_start = 10 * int(page_number)
    list_end = 10 * (int(page_number) + 1)
    objs = table.objects.all()[list_start:list_end]
    is_last = False
    if list_end >= len(table.objects.all()):
        is_last = True
    return render(request, 'pages/posts.html', {'objects': objs, 'page_number': page_number, 'is_last': is_last, 'table': table_name})  

def object_detailed(request, table_name, product_id):
    if table_name == 'inquiries':
        table = Inquiry
        obj = get_object_or_404(table, id=product_id)
        objs = Post.objects.get(id=obj.id)
    elif table_name == 'companies':
        table = Company
        obj = get_object_or_404(table, id=product_id)
        objs = Member.objects.filter(company=obj.name)
    elif table_name == 'members':
        table = Member
        obj = get_object_or_404(table, id=product_id)
        objs = Post.objects.filter(author = obj.username)
    else: 
        table = Post
        obj = get_object_or_404(table, id=product_id)
        objs = Comment.objects.all()

    return render(request, f'pages/{table_name}_details.html', {'object': obj, 'objects': objs})