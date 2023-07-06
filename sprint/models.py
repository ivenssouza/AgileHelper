from django.db import models
import uuid
from datetime import date

class Sprint(models.Model):
    class SprintType(models.TextChoices):
        DEV = 'DEV'
        UX = 'UX'
        SW = 'SW'

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, blank=False, null=False, choices=SprintType.choices)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=date.today, blank=True)

    class Meta:
        db_table = 'sprints'

    def __str__(self):
        return self.title

class Story(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE)
    ticket_number = models.PositiveIntegerField()
    description = models.CharField(max_length=200, blank=True)
    story_points = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'stories'
    
    def __str__(self):
        return str(self.ticket_number)
    