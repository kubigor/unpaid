from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=55)
    license_number = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=55)
    zip = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to="logos/")

    class Meta:
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name

class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    is_contractor = models.BooleanField(null=True)
    first_name = models.CharField(max_length=18)
    last_name = models.CharField(max_length=18)
    username = models.CharField(max_length=18, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=55, null=True)
    zip = models.CharField(max_length=5, null=True)
    company = models.CharField(max_length=55, null=True)

    def __str__(self):
        return self.username
    # company = models.ForeignKey(
    #     Company, related_name="company_member", on_delete=models.CASCADE, default=0)
    # position = models.CharField(choices=(
    #     ("Owner", "Owner"),
    #     ("Administrator", "Administrator"),
    #     ("Technician", "Technician"),
    #     ("Other", "Other"),)
    # )
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    service_provided = models.CharField(max_length=32)
    customer_info = models.TextField(max_length=200)
    invoice = models.CharField(max_length=18)
    amount = models.CharField(max_length=10)
    description = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Member, related_name="post_author", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    body = models.TextField(max_length=800)
    post = models.ForeignKey(Post, related_name="post_inquiry", on_delete=models.CASCADE)
    attachment = models.ImageField(null=True, upload_to="invoices/")
    author = models.ForeignKey(Member, related_name="inquiry_author", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = ("inquiries")

    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Member, related_name="comment_author", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    body = models.TextField(max_length=800)
    attachment = models.ImageField(null=True, upload_to="photos/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    