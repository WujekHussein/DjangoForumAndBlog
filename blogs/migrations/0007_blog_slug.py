# Generated by Django 5.1.4 on 2025-01-08 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_remove_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
