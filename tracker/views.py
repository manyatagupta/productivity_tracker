from django.shortcuts import render, redirect
from .models import Task  

def index(request):
    if request.method == 'POST':
        task_title = request.POST.get('title')
        
        task_priority = request.POST.get('priority') 
        
        
        if task_title:
             
            Task.objects.create(title=task_title, priority=task_priority)
            return redirect('index')
        # Is line ko delete waale logic ke niche add karein
        if request.GET.get('clear_completed'):
            Task.objects.filter(is_completed=True).delete()
            return redirect('index')
    

    if request.GET.get('complete'):
        task_id = request.GET.get('complete')
        task = Task.objects.get(id=task_id)
        task.is_completed = True
        task.save()
        return redirect('index')

    if request.GET.get('delete'):
        task_id = request.GET.get('delete')
        Task.objects.filter(id=task_id).delete()
        return redirect('index')

    # --- SEARCH LOGIC START ---
    search_query = request.GET.get('search', '')  # URL se 'search' keyword uthayega
    if search_query:
        # Agar search box mein kuch likha hai, toh wahi tasks filter honge
        tasks = Task.objects.filter(title__icontains=search_query).order_by('-created_at')
    else:
        # Agar search khali hai, toh purane tarike se saare tasks dikhenge
        tasks = Task.objects.all().order_by('-created_at')
    # --- SEARCH LOGIC END ---

    return render(request, 'tracker/index.html', {'tasks': tasks})