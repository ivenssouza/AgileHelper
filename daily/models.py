from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import User
from sprint.models import Sprint

class Daily(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    date = models.DateTimeField(default=date.today, blank=True)

    class Meta:
        db_table = 'dailies'

class Note(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    daily = models.ForeignKey(Daily, on_delete=models.CASCADE)
    ticket_number = models.IntegerField()
    overview = models.CharField(max_length=500)
    status = models.CharField(max_length=500)

    class Meta:
        db_table = 'notes'