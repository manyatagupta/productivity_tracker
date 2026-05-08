from django.shortcuts import render, redirect
from .models import Task  
from django.utils import timezone 
from django.contrib import messages 

def index(request):
    # 1. DARK MODE LOGIC (Session based)
    if request.GET.get('toggle_dark'):
        current_mode = request.session.get('dark_mode', False)
        request.session['dark_mode'] = not current_mode
        return redirect('index')

    dark_mode = request.session.get('dark_mode', False)

    # 2. POST LOGIC (Add Task with Auto-Emoji & Tags)
    if request.method == 'POST':
        task_title = request.POST.get('title')
        task_priority = request.POST.get('priority') 
        
        if task_title:
            # --- Auto-Emoji & Tag Logic ---
            emoji = ""
            tag = "General" # Default tag
            lower_title = task_title.lower()

            # Work Category
            if any(word in lower_title for word in ["code", "python", "django", "bug", "work"]): 
                emoji = "💻 "
                tag = "Work"
            # Study Category
            elif any(word in lower_title for word in ["study", "exam", "read", "learn"]): 
                emoji = "📚 "
                tag = "Study"
            # Meeting Category
            elif any(word in lower_title for word in ["meet", "call", "zoom"]): 
                emoji = "🤝 "
                tag = "Meet"
            # Food Category
            elif any(word in lower_title for word in ["food", "eat", "dinner", "pizza"]): 
                emoji = "🍕 "
                tag = "Food"
            # Health Category
            elif any(word in lower_title for word in ["gym", "workout", "health", "run"]): 
                emoji = "💪 "
                tag = "Health"
            # Shopping Category
            elif any(word in lower_title for word in ["buy", "shop", "amazon", "price"]): 
                emoji = "🛒 "
                tag = "Shop"
            # Finance Category
            elif "money" in lower_title or "pay" in lower_title:
                emoji = "💸 "
                tag = "Finance"
            
            # Final Title formatting with Tag
            final_title = f"[{tag}] {emoji}{task_title}"
            
            Task.objects.create(title=final_title, priority=task_priority)
            messages.success(request, f"New {tag} task added! 🚀")
            return redirect('index')

    # 3. CLEAR COMPLETED LOGIC (Enhanced)
    if request.GET.get('clear_completed'):
        completed_tasks_to_delete = Task.objects.filter(is_completed=True)
        count = completed_tasks_to_delete.count()
        
        if count > 0:
            completed_tasks_to_delete.delete()
            messages.success(request, f"Successfully cleared {count} completed tasks! 🧹")
        else:
            messages.info(request, "No completed tasks to clear.")
        return redirect('index')

    # 4. COMPLETE TASK LOGIC
    if request.GET.get('complete'):
        task_id = request.GET.get('complete')
        task = Task.objects.get(id=task_id)
        task.is_completed = True
        task.completed_at = timezone.now() 
        task.save()
        return redirect('index')

    # 5. DELETE TASK LOGIC
    if request.GET.get('delete'):
        task_id = request.GET.get('delete')
        task = Task.objects.get(id=task_id)
        task_title = task.title
        task.delete()
        messages.warning(request, f'Task "{task_title}" has been deleted!') 
        return redirect('index')

    # 5.5 EDIT TASK LOGIC 
    if request.GET.get('edit_id') and request.GET.get('new_title'):
        t_id = request.GET.get('edit_id')
        new_text = request.GET.get('new_title')
        try:
            task = Task.objects.get(id=t_id)
            task.title = new_text
            task.save()
            messages.success(request, f'Task updated successfully! ✨')
        except Task.DoesNotExist:
            pass
        return redirect('index')

    # 6. SEARCH LOGIC
    search_query = request.GET.get('search', '')
    
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query).order_by('priority', '-created_at')
    else:
        tasks = Task.objects.all().order_by('priority', '-created_at')

    # 7. PROGRESS & STATISTICS CALCULATION
    total_tasks = tasks.count()
    completed_tasks_count = tasks.filter(is_completed=True).count()
    pending_tasks_count = tasks.filter(is_completed=False).count() 
    
    progress_percent = 0
    if total_tasks > 0:
        progress_percent = int((completed_tasks_count / total_tasks) * 100)

    # 8. FINAL RENDER
    return render(request, 'tracker/index.html', {
        'tasks': tasks,
        'progress_percent': progress_percent, 
        'dark_mode': dark_mode,
        'pending_count': pending_tasks_count,      
        'completed_count': completed_tasks_count,         
    })