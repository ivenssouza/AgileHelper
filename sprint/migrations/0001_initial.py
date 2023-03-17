# Generated by Django 4.1.7 on 2023-03-08 19:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('DEV', 'Dev'), ('UX', 'Ux'), ('SW', 'Sw')], max_length=50)),
                ('number', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateTimeField(blank=True, default=datetime.date.today)),
            ],
            options={
                'db_table': 'sprints',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ticket_number', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('story_points', models.IntegerField()),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprint.sprint')),
            ],
            options={
                'db_table': 'stories',
            },
        ),
    ]
