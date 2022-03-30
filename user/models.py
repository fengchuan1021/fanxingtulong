from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    phone_number = models.CharField(max_length=20,null=True)
    wechatnickname=models.CharField(verbose_name='微信昵称',max_length=64,default='',null=True,blank=True)
    wechatid=models.CharField(verbose_name='微信id',max_length=64,default='',null=True,blank=True)
    tulong_endtime=models.DateTimeField(verbose_name='屠龙助手结束时间',blank=True,null=True)
    tulong_accout_numlimit=models.IntegerField(verbose_name='账号数量',default=5)
    tulongtryflag=models.BooleanField(verbose_name="屠龙助手已试用",default=False)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()