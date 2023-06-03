from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=55)
    license_number = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=55)
    zip = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to="logos/")

    class Meta:
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name

class Contractor(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(
        Company, related_name="company", on_delete=models.CASCADE)
    username = models.CharField(max_length=18, unique=True)
    first_name = models.CharField(max_length=18)
    last_name = models.CharField(max_length=18)
    email = models.EmailField(unique=True)
    position = models.CharField(choices=(
        ("Owner", "Owner"),
        ("Administrator", "Administrator"),
        ("Technician", "Technician"),
        ("Other", "Other"),)
    )

    def __str__(self):
        return self.name

class Customer(models.Model):
    username = models.CharField(max_length=18, unique=True)
    first_name = models.CharField(max_length=18)
    last_name = models.CharField(max_length=18)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=55)
    zip = models.CharField(max_length=5)

    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    body = models.TextField(max_length=800)
    post_id = models.CharField(max_length=10)
    attachment = models.ImageField(upload_to="invoices/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = ("inquiries")

    def __str__(self):
        return self.name

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.TextField(max_length=800)
    attachment = models.ImageField(upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    service_provided = models.CharField(max_length=32)
    customer_info = models.TextField(max_length=200)
    invoice = models.CharField(max_length=18)
    amount = models.CharField(max_length=10)
    description = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
