# Generated by Django 4.2.5 on 2023-09-18 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_tier'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tiers',
            new_name='Tier',
        ),
        migrations.AlterModelOptions(
            name='tier',
            options={'verbose_name': 'Tier', 'verbose_name_plural': 'Tiers'},
        ),
    ]
