from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ContractorChangeForm, CustomerChangeForm, CompanyCreationForm, LogoForm
from pages.models import Member, Company, Inquiry, Post
from base.selenium_scraper import find_status

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email %s is already registered.' % email)
            else:
                form.save()
                new_member = Member.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
                new_member.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/profile/type')
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
    current_member = Member.objects.get(username=request.user.username)
    current_user = User.objects.get(username=request.user.username)
    contractor = current_member.is_contractor
    if contractor:
        form = ContractorChangeForm(request.POST or None, instance=current_member)
    else:
        form = CustomerChangeForm(request.POST or None, instance=current_member)

    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            still_contractor = form.cleaned_data['is_contractor']
            print(still_contractor)
            current_member.first_name = first_name
            current_member.last_name = last_name
            current_member.email = email
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email
            if contractor != still_contractor:
                current_member.is_contractor = still_contractor
                if not still_contractor:
                    current_member.company = 'None'
                current_member.save()
                return redirect('/profile/settings')

            if contractor:
                company = form.cleaned_data['company']
                position = form.cleaned_data['position']
                current_member.company = company
                current_member.position = position
                if company == 'None':
                    current_member.save()
                    current_user.save()
                    messages.warning(request, "Every employee should be attached to the company. If your company is not listed create one!")
                    return render(request, 'profiles/profile_update.html', {'form': form})
            else:
                phone_number = form.cleaned_data['phone_number']
                address = form.cleaned_data['address']
                zip = form.cleaned_data['zip']
                current_member.phone_number = phone_number
                current_member.address = address
                current_member.zip = zip

            current_member.save()
            current_user.save()
            messages.success(request, "Changes have been applied!")
            
    return render(request, 'profiles/profile_update.html', {'form': form})

@login_required(login_url='/profile/login')
def profile(request):
    current_member = Member.objects.get(username=request.user.username)
    member_posts = Post.objects.filter(author=current_member.username)
    member_inquiries = Inquiry.objects.filter(author=current_member.id)
    company = current_member.company
    try:
        current_company = Company.objects.get(name=company)
    except:
        current_company = None
        to_render = {'current_member': current_member, 'posts': member_posts, 'inquiries': member_inquiries}

    if current_company:
        if request.method == 'POST':
            form = LogoForm(request.POST, request.FILES)
            if form.is_valid():
                current_company.image = form.cleaned_data['image']
                current_company.save()
        else:
            form = LogoForm()
        to_render = {'current_member': current_member, 'current_company': current_company, 'form': form, 'posts': member_posts, 'inquiries': member_inquiries}

    return render(request, 'profiles/profile.html', to_render)

def create_company(request):
    if request.method == 'POST':
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            current_member = Member.objects.get(username=request.user.username)
            company_name = form.cleaned_data['name']
            company_license = form.cleaned_data['license_number']
            current_member.company = company_name
            current_member.save()
            form.save()
            current_company = Company.objects.get(name=company_name)
            current_company.license_status = 'Active'
            # current_company.license_status = find_status(company_license)
            current_company.save()
            return redirect('/profile')
    else:
        form = CompanyCreationForm
    return render(request, 'profiles/create_company.html', {'form': form})

@login_required(login_url='/profile/login')
def type_option(request):
    profile = Member.objects.get(username=request.user.username)
    if 'contractor' in request.GET or 'customer' in request.GET:
        if 'contractor' in request.GET:
            profile.is_contractor = True
        elif 'customer' in request.GET:
            profile.is_contractor = False
        profile.save()
        return redirect('/profile/settings')
    return render(request, 'profiles/contractor_customer.html')

def update_status(request):
    current_member = Member.objects.get(username=request.user.username)
    try:
        current_company = Company.objects.get(name=current_member.company)
    except:
        return redirect('/profile')
    company_license = current_company.license_number
    current_company.license_status = find_status(company_license)
    if current_company.license_status == "Active":
        messages.success(request, f"Your status is {current_company.license_status}")
    current_company.save()
    return redirect('/profile')
