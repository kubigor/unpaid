from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from pages.models import Member, Company

class CompanyCreationForm(ModelForm):
    required_css_class = 'form-label'

    name = forms.CharField(max_length=55)
    license_number = forms.CharField(max_length=12)
    address = forms.CharField(max_length=55)
    zip = forms.CharField(max_length=5)
    phone_number = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=55)

    class Meta:
        model = Company
        fields = ('name', 'license_number', 'address', 'zip', 'phone_number', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None


class UserRegistrationForm(UserCreationForm):
    required_css_class = 'form-label'
    
    email = forms.EmailField(max_length=55)
    first_name = forms.CharField(max_length=18)
    last_name = forms.CharField(max_length=18)

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
    email = forms.EmailField(max_length=55)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=55)    
    zip = forms.CharField(max_length=5)
    is_contractor = forms.ChoiceField

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'zip', 'is_contractor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None


class ContractorChangeForm(UserChangeForm):
    password = None
    required_css_class = 'form-label'
    
    email = forms.EmailField(max_length=55)
    first_name = forms.CharField(max_length=18)
    last_name = forms.CharField(max_length=18)
    company = forms.ChoiceField
    position = forms.ChoiceField
    is_contractor = forms.ChoiceField

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'company', 'position', 'is_contractor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None


class LogoForm(ModelForm):
    required_css_class = 'form-label'

    class Meta:
        model = Company
        fields = ('image',)
        labels = {'image': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs.update({'class': 'image-field', 'id': 'logo-update'})
