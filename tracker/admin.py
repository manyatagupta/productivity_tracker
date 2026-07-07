from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'is_completed', 'due_date', 'created_at')
    list_filter = ('is_completed', 'priority', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Status & Priority', {
            'fields': ('priority', 'is_completed', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
