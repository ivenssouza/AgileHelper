from django.db import models
import uuid
from django.contrib.auth.models import User

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'participants'
