from django.contrib import admin
from .models import Company, Member, Post, Inquiry

admin.site.register(Company)
admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Inquiry)

