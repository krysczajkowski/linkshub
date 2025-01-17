# Generated by Django 3.2.3 on 2021-05-28 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appearance', '0008_usertheme_custom_background_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='ButtonTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('background_color', models.CharField(blank=True, max_length=100)),
                ('font_color', models.CharField(blank=True, max_length=100)),
                ('is_premium', models.BooleanField(default=False)),
            ],
        ),
    ]
