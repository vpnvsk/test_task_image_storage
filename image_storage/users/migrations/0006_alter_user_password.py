# Generated by Django 4.2.5 on 2023-09-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_thumbnail_tier_expiring_link_tier_original_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(),
        ),
    ]
