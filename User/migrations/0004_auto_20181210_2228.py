# Generated by Django 2.1.3 on 2018-12-10 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20181125_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='QQ',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='snum',
            field=models.IntegerField(default=0),
        ),
    ]
