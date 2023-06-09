from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ContractorChangeForm, CustomerChangeForm
from pages.models import Member

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
                id = User.objects.get(username=username).id
                new_member = Member.objects.create(id=id, first_name=first_name, last_name=last_name, username=username, email=email)
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
            current_member.first_name = first_name
            current_member.last_name = last_name
            current_member.email = email
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.email = email

            if contractor:
                company = form.cleaned_data['company']
                current_member.company = company
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
    username = current_member.username
    first_name = current_member.first_name
    last_name = current_member.last_name
    email = current_member.email
    phone_number = current_member.phone_number
    address = current_member.address
    zip = current_member.zip
    company = current_member.company

    return render(request, 'profiles/profile.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number, 'address': address, 'zip': zip, 'company': company})

@login_required(login_url='/profile/login')
def type_option(request):
    return render(request, 'profiles/contractor_customer.html')

@login_required(login_url='/profile/login')
def set_type(request, type):
    profile = Member.objects.get(username=request.user.username)
    if type == 'contractor':
        profile.is_contractor = True
    else:
        profile.is_contractor = False
    profile.save()
    return redirect('/profile/settings')
