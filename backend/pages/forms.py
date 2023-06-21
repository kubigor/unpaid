from django import forms
from django.forms import ModelForm
from .models import Post, Inquiry, Comment

class PostForm(ModelForm):
    required_css_class = 'form-label'
    
    invoice_photo = forms.FileField

    class Meta:
        model = Post
        widgets = {'customer_info': forms.Textarea(attrs={'style':'resize:none;'}),
                   'description': forms.Textarea(attrs={'style':'resize:none;'})}
        
        fields = ('title', 'service_provided', 'customer_info', 'invoice_number', 'amount', 'description', 'invoice_photo')
        labels = {'invoice_photo': 'Invoice photo/file'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})

class InquiryForm(ModelForm):
    required_css_class = 'form-label'
    
    attachment = forms.FileField(required=False, label='')
    
    class Meta:
        model = Inquiry
        widgets = {'body': forms.Textarea(attrs={'style':'resize:none; max-height: none;'})}
        fields = ('title', 'post', 'body', 'attachment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-field'})
        self.fields['attachment'].widget.attrs.update({'class': 'attachment'})


class CommentForm(ModelForm):
    
    attachment = forms.FileField(required=False, label='')

    class Meta:
        model = Comment
        widgets = {'body': forms.Textarea(attrs={'placeholder':'Leave your comment!'})}
        fields = ('body', 'attachment')
        labels = {'body': ''}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['attachment'].widget.attrs.update({'class': 'attachment'})

