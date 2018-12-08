# Generated by Django 2.1.3 on 2018-11-25 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='userId',
        ),
        migrations.AddField(
            model_name='user',
            name='fobNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='recTime',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('男', '男性'), ('女', '女性'), ('未知', '性别未知')], default='未知', max_length=2),
        ),
    ]