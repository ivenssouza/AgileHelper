# Generated by Django 4.1.7 on 2023-03-13 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0006_alter_story_story_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='planning_id',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
    ]
