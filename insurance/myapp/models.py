from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    photo=models.ImageField(upload_to='image/',null=True)

    def __str__(self):
        return self.user.username

class Campaign(models.Model):
    campaignname=models.CharField(max_length=200,null=True)
    place=models.CharField(max_length=200,null=True)
    time=models.TimeField(null=True, blank=True)
    image=models.ImageField(upload_to='image/',null=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

class Client(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar = models.CharField(max_length=12)
    pan = models.CharField(max_length=10)
    income = models.PositiveIntegerField()
    children = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    other_policy = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    address = models.TextField()
    job = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    dob = models.DateField()
    rate = models.PositiveIntegerField()

    def __str__(self):
        return self.name


