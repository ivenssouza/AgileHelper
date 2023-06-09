# Generated by Django 4.1.7 on 2023-03-08 19:37

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sprint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.date.today)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprint.sprint')),
            ],
            options={
                'db_table': 'dailies',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('ticket_number', models.IntegerField()),
                ('overview', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=500)),
                ('daily', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily.daily')),
            ],
            options={
                'db_table': 'notes',
            },
        ),
    ]
