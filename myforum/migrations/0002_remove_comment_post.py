# Generated by Django 2.0.9 on 2019-01-02 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myforum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
    ]
