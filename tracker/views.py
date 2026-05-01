from django.shortcuts import render, redirect
from .models import Task

def index(request):
    if request.method == 'POST':
        task_title = request.POST.get('title')
        if task_title:
            Task.objects.create(title=task_title)
            return redirect('index')

    if request.GET.get('complete'):
        task_id = request.GET.get('complete')
        task = Task.objects.get(id=task_id)
        task.is_completed = True
        task.save()
        return redirect('index')

    # NAYA DELETE LOGIC
    if request.GET.get('delete'):
        task_id = request.GET.get('delete')
        Task.objects.filter(id=task_id).delete()
        return redirect('index')

    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tracker/index.html', {'tasks': tasks})