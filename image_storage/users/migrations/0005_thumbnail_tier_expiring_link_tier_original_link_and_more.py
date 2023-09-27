# Generated by Django 4.2.5 on 2023-09-24 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_options_user_tier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Thumbnail',
                'verbose_name_plural': 'Thumbnails',
            },
        ),
        migrations.AddField(
            model_name='tier',
            name='expiring_link',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tier',
            name='original_link',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tier',
            name='thumbnail_size',
            field=models.ManyToManyField(to='users.thumbnail'),
        ),
    ]
