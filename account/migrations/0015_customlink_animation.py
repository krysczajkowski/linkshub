# Generated by Django 3.2.3 on 2021-06-22 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_remove_customlink_animation'),
    ]

    operations = [
        migrations.AddField(
            model_name='customlink',
            name='animation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.linkanimation'),
        ),
    ]
