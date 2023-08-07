from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import PostForm, InquiryForm, CommentForm
from .models import Post, Member, Inquiry, Company, Comment

@login_required(login_url='/profile/login')
def create_post(request):
    member = Member.objects.get(username=request.user.username)
    company_status = False
    if member.is_contractor and member.company != 'None':
        company_status = True if Company.objects.get(name=member.company).license_status == 'Active' else False
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
        
    return render(request, 'pages/newpost.html', {'form':form, 'submitted': submitted, 'member': member, 'company_status': company_status})

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

@login_required(login_url='/profile/login')
def search(request, table_name, page_number=0):
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

@login_required(login_url='/profile/login')
def search_results(request):
    table_name = 'posts'
    if request.method == "POST":
        search = request.POST['search']
        results = Post.objects.filter(Q(title__contains=search) | Q(service_provided__contains=search) | Q(customer_info__contains=search) | Q(invoice_number__contains=search) | Q(amount__contains=search) | Q(description__contains=search))
    else:
        redirect('/')
    return render(request, 'pages/results.html', {'table': table_name, 'results': results})

def object_detailed(request, table_name, product_id):

    if table_name == 'inquiries':
        table = Inquiry
        obj = get_object_or_404(table, id=product_id)
        objs = Post.objects.get(id=obj.id)
        member = obj.author
        post = Post.objects.get(title=obj.post)
        return render(request, f'pages/{table_name}_details.html', {'object': obj, 'objects': objs, 'post': post, 'member': member})

    elif table_name == 'companies':
        table = Company
        obj = get_object_or_404(table, id=product_id)
        objs = Member.objects.filter(company=obj.name)
        return render(request, f'pages/{table_name}_details.html', {'object': obj, 'objects': objs})
    
    elif table_name == 'members':
        table = Member
        obj = get_object_or_404(table, id=product_id)
        objs = Post.objects.filter(author = obj.username)
        member_posts = Post.objects.filter(author=obj.username)
        member_inquiries = Inquiry.objects.filter(author=obj.id)
        return render(request, f'pages/{table_name}_details.html', {'object': obj, 'objects': objs, 'posts': member_posts, 'inquiries': member_inquiries})
    
    elif table_name == 'posts':
        table = Post
        obj = get_object_or_404(table, id=product_id)
        post_author = Member.objects.get(username=obj.author)
        comments = Comment.objects.filter(post=obj)
        current_user = str(request.user.username)

        if request.method == "POST":
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = Member.objects.get(username=request.user.username)
                new_comment.post = obj
                new_comment.save()
                form = CommentForm()
                return HttpResponseRedirect(request.path)
        else:
            form = CommentForm()  
        return render(request, f'pages/{table_name}_details.html', {'form': form, 'object': obj, 'post_author': post_author, 'current_user': current_user, 'comments': comments, 'path': request.path})
    
def delete_comment(request, post_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return HttpResponseRedirect(f'/posts/{post_id}')