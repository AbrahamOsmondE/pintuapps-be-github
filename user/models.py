from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.management.utils import get_random_secret_key

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_superuser(self,email,password,**other_fields):
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_active',True)
        if other_fields.get('is_staff') is False:
            raise ValueError("Superuser must assign is_staff to True")
        if other_fields.get("is_superuser") is False:
            raise ValueError("Superuser must assign is_superuser to True")
        return self.create_user(email,password,**other_fields)

    def create_user(self,email,password,google_id,**other_fields):
        if not email:
            raise ValueError("Please provide a email!")
        if not google_id:
            raise ValueError("Please provide google id!")
        email = self.normalize_email(email=email)
        user = self.model(email=email,google_id=google_id,**other_fields)
        if not password:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.full_clean()
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    TYPE = (
        ('buyer','buyer'),
        ('seller','seller'),
        ('admin','admin'),
        ('not_registered','not_registered')
    )
    email = models.EmailField(unique=True)
    google_id = models.CharField(max_length=50, unique=True, default="google_id")
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)
    secret_otp = models.CharField(max_length=255, default="secret_otp")
    user_type = models.CharField(max_length=15,choices=TYPE,default="not_registered")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    voting_verified = models.BooleanField(default=False)
    voting_secret_key = models.CharField(max_length=255, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['google_id']

class Buyer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    name= models.CharField(max_length=100)
    ntu_email= models.EmailField(max_length=100, unique=True)
    contact_number=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)
    birth_date=models.CharField(max_length=50)
    course=models.CharField(max_length=100)
    graduation_year=models.IntegerField()
    address=models.TextField()
    origin_city=models.CharField(max_length=100)
    company=models.CharField(max_length=200)
    emergency_name=models.CharField(max_length=100, default="")
    emergency_contact=models.CharField(max_length=30, default="")

class Seller(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    name=models.CharField(max_length=100)
    contact_number=models.CharField(max_length=30)
    gender=models.CharField(max_length=30)
