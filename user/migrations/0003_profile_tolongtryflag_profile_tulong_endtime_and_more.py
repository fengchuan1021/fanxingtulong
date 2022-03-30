# Generated by Django 4.0.3 on 2022-03-24 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tolongtryflag',
            field=models.BooleanField(default=False, verbose_name='屠龙助手已试用'),
        ),
        migrations.AddField(
            model_name='profile',
            name='tulong_endtime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='屠龙助手结束时间'),
        ),
        migrations.AddField(
            model_name='profile',
            name='wechatid',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='微信id'),
        ),
        migrations.AddField(
            model_name='profile',
            name='wechatnickname',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='微信昵称'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]