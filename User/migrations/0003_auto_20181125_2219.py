# Generated by Django 2.1.3 on 2018-11-25 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20181125_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]