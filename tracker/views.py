from django.shortcuts import render, redirect
from .models import Task  

def index(request):
    # 1. DARK MODE LOGIC (Session based)
    if request.GET.get('toggle_dark'):
        current_mode = request.session.get('dark_mode', False)
        request.session['dark_mode'] = not current_mode
        return redirect('index')

    dark_mode = request.session.get('dark_mode', False)

    # 2. POST LOGIC (Add Task)
    if request.method == 'POST':
        task_title = request.POST.get('title')
        task_priority = request.POST.get('priority') 
        
        if task_title:
            Task.objects.create(title=task_title, priority=task_priority)
            return redirect('index')

    # 3. CLEAR COMPLETED LOGIC (Bulk Delete)
    if request.GET.get('clear_completed'):
        Task.objects.filter(is_completed=True).delete()
        return redirect('index')

    # 4. COMPLETE TASK LOGIC
    if request.GET.get('complete'):
        task_id = request.GET.get('complete')
        task = Task.objects.get(id=task_id)
        task.is_completed = True
        task.save()
        return redirect('index')

    # 5. DELETE TASK LOGIC
    if request.GET.get('delete'):
        task_id = request.GET.get('delete')
        Task.objects.filter(id=task_id).delete()
        return redirect('index')

    # 6. SEARCH LOGIC
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(title__icontains=search_query).order_by('-created_at')
    else:
        tasks = Task.objects.all().order_by('-created_at')

    # 7. PROGRESS CALCULATION
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    
    if total_tasks > 0:
        progress_percent = int((completed_tasks / total_tasks) * 100)
    else:
        progress_percent = 0

    # 8. FINAL RENDER (Sirf ek baar, sabse aakhir mein)
    return render(request, 'tracker/index.html', {
        'tasks': tasks,
        'progress_percent': progress_percent,
        'dark_mode': dark_mode
    })