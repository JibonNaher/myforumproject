# Generated by Django 2.0.9 on 2019-01-02 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myforum', '0004_auto_20190102_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myforum.Post'),
        ),
    ]