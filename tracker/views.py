from django.shortcuts import render, redirect
from .models import Task  
from django.utils import timezone 
from django.contrib import messages 
from datetime import timedelta 

def index(request):
    # 1. DARK MODE LOGIC
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
            emoji = ""
            tag = "General"
            lower_title = task_title.lower()

            # Smart Tagging Logic
            mapping = {
                "Work": ["code", "python", "django", "bug", "work", "assign"],
                "Study": ["study", "exam", "read", "learn"],
                "Meet": ["meet", "call", "zoom", "meeting"],
                "Food": ["food", "eat", "dinner", "pizza"],
                "Health": ["gym", "workout", "health", "run"],
                "Shop": ["buy", "shop", "amazon", "price"],
                "Finance": ["money", "pay", "bank"]
            }
            emojis = {"Work": "💻 ", "Study": "📚 ", "Meet": "🤝 ", "Food": "🍕 ", "Health": "💪 ", "Shop": "🛒 ", "Finance": "💸 "}

            for t, keywords in mapping.items():
                if any(word in lower_title for word in keywords):
                    tag = t
                    emoji = emojis.get(t, "")
                    break
            
            final_title = f"[{tag}] {emoji}{task_title}"
            Task.objects.create(title=final_title, priority=task_priority)
            messages.success(request, f"New {tag} task added! 🚀")
            return redirect('index')

    # 3. COMPLETE/DELETE/EDIT LOGIC (Sab ek saath)
    if request.GET.get('complete'):
        task = Task.objects.filter(id=request.GET.get('complete')).first()
        if task:
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()
            messages.success(request, "BOOM! Task Completed! 🎉")
        return redirect('index')

    if request.GET.get('delete'):
        Task.objects.filter(id=request.GET.get('delete')).delete()
        messages.warning(request, "Task deleted!")
        return redirect('index')

    if request.GET.get('clear_completed'):
        Task.objects.filter(is_completed=True).delete()
        return redirect('index')

    # --- COMMIT 3: SEARCH, FILTER & STATS ---
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')
    
    tasks = Task.objects.all()

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    
    if filter_type == 'high':
        tasks = tasks.filter(priority='high', is_completed=False)
    elif filter_type == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif filter_type == 'completed':
        tasks = tasks.filter(is_completed=True)

    tasks = tasks.order_by('priority', '-created_at')

    # Statistics Calculation
    total_tasks = Task.objects.count()
    completed_tasks_count = Task.objects.filter(is_completed=True).count()
    today = timezone.now().date()
    tasks_done_today = Task.objects.filter(completed_at__date=today, is_completed=True).count()
    tasks_created_today = Task.objects.filter(created_at__date=today).count()
    
    today_score = f"{tasks_done_today}/{tasks_created_today}" if tasks_created_today > 0 else "0/0"
    progress_percent = int((completed_tasks_count / total_tasks * 100)) if total_tasks > 0 else 0

    return render(request, 'tracker/index.html', {
        'tasks': tasks,
        'progress_percent': progress_percent, 
        'dark_mode': dark_mode,
        'today_score': today_score,
        'search_query': search_query,
        'filter_type': filter_type, # <-- FIXED: For active button styling
        'now': timezone.now(),        
    })