from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Inquiry, Customer, Company

class PostForm(ModelForm):
    required_css_class = 'form-label'
    
    class Meta:
        model = Post
        widgets = {'customer_info': forms.Textarea(attrs={'style':'resize:none;'}),
                   'description': forms.Textarea(attrs={'style':'resize:none;'})}
        fields = ('title', 'service_provided', 'customer_info', 'invoice', 'amount', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})

class CompanyForm(UserCreationForm):    
    name = forms.CharField(max_length=55)
    license_number = forms.CharField(max_length=12)
    approved = forms.BooleanField()
    address = forms.CharField(max_length=55)
    zip = forms.CharField(max_length=5)
    phone_number = forms.CharField(max_length=10)
    image = forms.ImageField()

    class Meta:
        model = Company
        fields = ('name', 'license_number', 'approved', 'address', 'zip', 'phone_number' ,'image')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)


# class InquiryForm(ModelForm):
#     required_css_class = 'form-label'
    
#     class Meta:
#         model = Post
#         fields = ('title', 'service_provided', 'customer_info', 'invoice', 'amount', 'description')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-field'})

