from django.db import models
from user.models import User

# Create your models here.
class Voted(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)

class Ballot(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    candidate = models.CharField(max_length=100)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    motto = models.TextField()
    display_picture = models.TextField()