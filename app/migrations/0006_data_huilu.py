# Generated by Django 2.1.7 on 2019-09-26 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20190924_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='huilu',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
