from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from pages.models import Member

class UserRegistrationForm(UserCreationForm):
    required_css_class = 'form-label'
    
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None

class CustomerChangeForm(UserChangeForm):
    password = None
    required_css_class = 'form-label'
    
    first_name = forms.CharField(max_length=18)
    last_name = forms.CharField(max_length=18)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=55)    
    zip = forms.CharField(max_length=5)

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'zip')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None


class ContractorChangeForm(UserChangeForm):
    password = None
    required_css_class = 'form-label'
    
    email = forms.EmailField()
    first_name = forms.CharField(max_length=18)
    last_name = forms.CharField(max_length=18)
    company = forms.CharField(max_length=18)

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'company')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None