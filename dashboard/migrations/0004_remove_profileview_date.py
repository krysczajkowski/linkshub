# Generated by Django 3.2.3 on 2021-06-20 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_profileview_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileview',
            name='date',
        ),
    ]