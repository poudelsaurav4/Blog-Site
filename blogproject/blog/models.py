from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
# Create your models here.
from .manager import BloguserManager

class Bloguser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    GENDER_CHOICES = (
        ('M', 'Hale'),
        ('F', 'Female'),
        ('O', 'other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default= timezone.now)

    objects = BloguserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return self.username
    
class Createblog(models.Model):
    user = models.ForeignKey(Bloguser, on_delete= models.CASCADE, related_name= 'user')
    title = models.TextField(max_length=256)
    description = models.TextField()
    blog_img = models.ImageField(upload_to='media/', blank=True)
    published_on = models.DateField(default= timezone.now)
    edited_on = models.DateField(default=timezone.now)



    def __str__(self) -> str:
        return self.title