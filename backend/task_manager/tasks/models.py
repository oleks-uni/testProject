from datetime import datetime, timezone
from django.db import models
from users.models import UserModel


class TaskModel(models.Model):
    title = models.CharField(max_length=55, unique=True)
    description = models.TextField(max_length=155)

    created_at = models.DateTimeField(default=datetime.now(timezone.utc),)
    updated_at = models.DateTimeField(default=datetime.now(timezone.utc),)

    is_completed = models.BooleanField(default=False,)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title