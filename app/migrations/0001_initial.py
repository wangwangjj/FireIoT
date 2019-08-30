# Generated by Django 2.1.7 on 2019-08-30 05:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('huilu', models.CharField(max_length=200)),
                ('addr', models.CharField(max_length=200)),
                ('item', models.TextField()),
                ('state', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'FireData',
                'ordering': ('-pub_date',),
            },
        ),
    ]
