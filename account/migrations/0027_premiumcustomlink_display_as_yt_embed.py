# Generated by Django 3.2.3 on 2021-11-20 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_remove_profile_linkshub_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumcustomlink',
            name='display_as_yt_embed',
            field=models.BooleanField(default=False),
        ),
    ]