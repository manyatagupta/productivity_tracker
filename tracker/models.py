from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, default='medium')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # 🔥 ERROR FIX: Add these two lines here
    description = models.TextField(blank=True, default='')
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title