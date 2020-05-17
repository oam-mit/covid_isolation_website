from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save


# Create your models here.
@receiver(post_save,sender=User)
def create_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)