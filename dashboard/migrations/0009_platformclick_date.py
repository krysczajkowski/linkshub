# Generated by Django 3.2.5 on 2021-07-04 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_linkclick_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformclick',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
