from django.contrib import admin
from .models import Company, Contractor, Customer, Post, Inquiry

admin.site.register(Company)
admin.site.register(Contractor)
admin.site.register(Customer)
admin.site.register(Post)
admin.site.register(Inquiry)

