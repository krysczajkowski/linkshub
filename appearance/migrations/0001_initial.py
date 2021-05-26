# Generated by Django 3.2.3 on 2021-05-24 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bg_class_name', models.CharField(max_length=100)),
                ('link_class_name', models.CharField(max_length=100)),
                ('is_premium', models.BooleanField(default=False)),
            ],
        ),
    ]
