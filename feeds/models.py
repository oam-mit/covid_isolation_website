from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.
class Feed(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(null=True,blank=True)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name


from django.utils.text import slugify
@receiver(pre_save,sender=Feed)
def make_slug(sender,instance=None,**kwargs):
    instance.slug=slugify(instance.name)