from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import User
from sprint.models import Sprint, Story

class Planning(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=date.today, blank=True)

    class Meta:
        db_table = 'plannings'
    
    def __str__(self):
        return str(self.id)

class PlanningParticipant(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    planning = models.ForeignKey(Planning, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'planning_participants'

class PokerRound(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    planning = models.ForeignKey(Planning, on_delete=models.CASCADE, blank=True, null=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True)
    avg_points = models.PositiveIntegerField(blank=True, null=True)
    open = models.BooleanField(default=True)

    class Meta:
        db_table = 'poker_rounds'

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    poker_round = models.ForeignKey(PokerRound, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    estimated_points = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'votes'