# Generated by Django 4.1.7 on 2023-03-13 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planning', '0005_alter_pokerround_avg_points_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]