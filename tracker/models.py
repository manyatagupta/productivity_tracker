from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=10, default='high')

    def __str__(self):
        return self.title
