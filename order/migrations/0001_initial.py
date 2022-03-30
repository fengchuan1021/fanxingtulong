# Generated by Django 4.0.3 on 2022-03-23 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernum', models.CharField(db_index=True, max_length=128, verbose_name='订单号')),
                ('money', models.FloatField(default=0, verbose_name='金额')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('product', models.CharField(db_index=True, max_length=32, verbose_name='产品')),
                ('num', models.IntegerField(default=0, verbose_name='数量')),
                ('time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='时间')),
            ],
        ),
    ]