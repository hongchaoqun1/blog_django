from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE )
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return "username %s"%self.user.username

class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=64, null=True)
    company = models.CharField(max_length=64, null=True)
    profession = models.CharField(max_length=64, null=True)
    address = models.CharField(max_length=64, null=True)
    aboutme = models.TextField(null=True)

    def __str__(self):
        return  "username %s"%self.user.username
