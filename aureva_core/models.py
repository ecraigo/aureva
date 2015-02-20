from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    level = models.IntegerField(default=1)
    style = models.CharField(max_length=128, default='')
    biography = models.TextField(default='')