from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks',
        null=True, 
        blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    priority = models.CharField(
        max_length=10, 
        choices=PriorityChoices.choices, 
        default=PriorityChoices.MEDIUM
    )
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title