from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=55)
    license_number = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=55)
    zip = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    license_status = models.CharField(max_length=55)
    image = models.ImageField(null=True, upload_to="logos/")

    class Meta:
        verbose_name_plural = ("companies")

    def __str__(self):
        return self.name



class Member(models.Model):
    def company_filler():
        try:
            companies = Company.objects.all()
            choices = [('None', 'Not on the list')]
            for unit in companies:
                choices.append((f"{unit}", f"{unit}"))
            return tuple(choices)
        except:
            return (('None', 'Not on the list'),)
    
    id = models.AutoField(primary_key=True)
    is_contractor = models.BooleanField(default=False, choices=(
        (True, "Yes"),
        (False, "No")))
    first_name = models.CharField(max_length=18)
    last_name = models.CharField(max_length=18)
    username = models.CharField(max_length=18, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=55, null=True)
    zip = models.CharField(max_length=5, null=True)
    company = models.CharField(default='None', choices=(company_filler()))
    position = models.CharField(default='Other', choices=(
        ("Owner", "Owner"),
        ("Administrator", "Administrator"),
        ("Technician", "Technician"),
        ("Other", "Other"),)
    )

    def __str__(self):
        return self.username
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    service_provided = models.CharField(max_length=32)
    customer_info = models.TextField(max_length=200)
    invoice_number = models.CharField(max_length=18)
    invoice_photo = models.ImageField(default='', upload_to="invoices")
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=55)

    def __str__(self):
        return self.title
    
    
class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    body = models.TextField(max_length=800)
    post = models.ForeignKey(Post, related_name="post_inquiry", on_delete=models.CASCADE)
    attachment = models.ImageField(null=True, upload_to="photos/")
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
        return str(self.post.title) + ' comment'
    