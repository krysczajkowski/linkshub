# Generated by Django 3.2.3 on 2021-08-28 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appearance', '0017_alter_custombackgroundtheme_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombackgroundtheme',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='background_image'),
        ),
    ]
