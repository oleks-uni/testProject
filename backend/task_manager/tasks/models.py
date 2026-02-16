from django.utils import timezone
from django.db import models
from users.models import UserModel


class TaskModel(models.Model):
    title = models.CharField(max_length=55, unique=True)
    description = models.TextField(max_length=155)

    created_at = models.DateTimeField(default=timezone.now,)
    updated_at = models.DateTimeField(auto_now=True,)

    is_completed = models.BooleanField(default=False,)
    completed_at = models.DateTimeField(default=None, null=True, blank=True)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.is_completed:
            self.completed_at = timezone.now()
        else:
            self.completed_at = None

        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.title