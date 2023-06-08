from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

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

class ProfileChangeForm(UserChangeForm):
    password = None
    required_css_class = 'form-label'
    
    email = forms.EmailField()
    first_name = forms.CharField(max_length=18)
    last_name = forms.CharField(max_length=18)
    phone_number = forms.CharField(max_length=10)
    address = forms.CharField(max_length=55)
    zip = forms.CharField(max_length=5)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
            self.fields[field].help_text = None