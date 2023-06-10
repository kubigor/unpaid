from django import forms
from django.forms import ModelForm
from .models import Post, Inquiry

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

class InquiryForm(ModelForm):
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
