from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4



class Users(AbstractUser):
    id        = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    email       = models.CharField(max_length=125,null=False,unique=True)
    first_name  = models.CharField(max_length=255,null=False)
    last_name   = models.CharField(max_length=125,null=False)
    is_seller   = models.BooleanField(null=False)
    is_admin    = models.BooleanField(default=False)
    username    = None



    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []