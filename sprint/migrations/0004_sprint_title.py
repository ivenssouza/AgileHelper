# Generated by Django 4.1.7 on 2023-03-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0003_alter_sprint_number_alter_story_story_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='title',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
