from django.shortcuts import render, redirect
from .models import Task
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
import re


# ─── Smart Tag + Emoji Mapping ───────────────────────────────────────────────

TAG_KEYWORDS = {
    "Work":     ["code", "python", "django", "bug", "work", "assign", "deploy", "review", "pr", "task"],
    "Study":   ["study", "exam", "read", "learn", "course", "notes", "chapter", "revise"],
    "Meet":    ["meet", "call", "zoom", "meeting", "standup", "sync", "discuss"],
    "Food":    ["food", "eat", "dinner", "pizza", "lunch", "breakfast", "cook", "order"],
    "Health":  ["gym", "workout", "health", "run", "walk", "exercise", "medicine", "doctor"],
    "Shop":    ["buy", "shop", "amazon", "order", "purchase", "cart"],
    "Finance": ["money", "pay", "bank", "bill", "upi", "transfer", "salary", "expense"],
}

TAG_EMOJIS = {
    "Work": "💻",
    "Study": "📚",
    "Meet": "🤝",
    "Food": "🍕",
    "Health": "💪",
    "Shop": "🛒",
    "Finance": "💸",
    "General": "📌",
}

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def get_tag_for_title(title: str) -> str:
    lower = title.lower()
    for tag, keywords in TAG_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return tag
    return "General"


def get_motivation_quote(tasks_created: int, tasks_done: int, pct: int) -> str:
    if tasks_created == 0:
        return "No tasks yet today — clean slate, endless possibilities! ✨"
    if tasks_done == tasks_created:
        return "Absolute champion status! 100% completion achieved 👑"
    if pct >= 75:
        return "Almost there! One final push. 🔥"
    if pct >= 50:
        return "More than halfway! Momentum is on your side ⚡"
    if pct >= 25:
        return "Solid start — keep the engine running 🏗️"
    return "Small progress is still progress. Let's go! 💪"


# ─── Main View ───────────────────────────────────────────────────────────────

def index(request):

    # 1. DARK MODE TOGGLE
    if request.GET.get('toggle_dark'):
        request.session['dark_mode'] = not request.session.get('dark_mode', False)
        return redirect('index')

    dark_mode = request.session.get('dark_mode', False)

    # 2. ADD TASK (POST)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        priority = request.POST.get('priority', 'medium')

        if title:
            tag = get_tag_for_title(title)
            emoji = TAG_EMOJIS.get(tag, "📌")
            final_title = f"[{tag} {emoji}] {title}"
            Task.objects.create(title=final_title, priority=priority)
            messages.success(request, f"✅ New {tag} task added!")
            return redirect('index')

    # 3. ACTIONS (GET params)
    action_id = request.GET.get('complete') or request.GET.get('delete')

    if request.GET.get('complete'):
        task = Task.objects.filter(id=request.GET['complete']).first()
        if task and not task.is_completed:
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()
            messages.success(request, "BOOM! Task completed! 🎉")
        return redirect('index')

    if request.GET.get('delete'):
        deleted, _ = Task.objects.filter(id=request.GET['delete']).delete()
        if deleted:
            messages.warning(request, "Task removed.")
        return redirect('index')

    # FEATURE: Archive completed tasks instead of deleting them hard
    if request.GET.get('archive_completed'):
        # Assuming your model has an 'is_archived' field or handling it dynamically via sessions/titles
        # For a clean approach without migrations, we append an internal tag string
        completed_tasks = Task.objects.filter(is_completed=True)
        count = 0
        for t in completed_tasks:
            if not t.title.endswith(" [ARCHIVED]"):
                t.title = f"{t.title} [ARCHIVED]"
                t.save()
                count += 1
        messages.info(request, f"Archived {count} completed task(s) successfully.")
        return redirect('index')

    if request.GET.get('clear_all_tasks_master'):
        Task.objects.all().delete()
        messages.error(request, "All tasks cleared! 🧹")
        return redirect('index')

    # 4. SEARCH + FILTER + SORTING
    search_query = request.GET.get('search', '').strip()
    filter_type  = request.GET.get('filter', 'all')
    sort_by      = request.GET.get('sort', 'default')
    selected_tag = request.GET.get('tag', 'all')
    view_archived = request.GET.get('view_archived', '0') == '1'

    tasks = Task.objects.all()

    # Dynamic separation of archived vs active items
    if view_archived:
        tasks = tasks.filter(title__icontains="[ARCHIVED]")
    else:
        tasks = tasks.exclude(title__icontains="[ARCHIVED]")

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    if filter_type == 'high':
        tasks = tasks.filter(priority='high', is_completed=False)
    elif filter_type == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif filter_type == 'completed':
        tasks = tasks.filter(is_completed=True)

    if selected_tag and selected_tag != 'all':
        tasks = tasks.filter(title__startswith=f"[{selected_tag}")

    # Smart Conditional Sorting Engine
    if sort_by == 'latest':
        tasks = tasks.order_by('-created_at')
    else:
        tasks = sorted(
            tasks,
            key=lambda t: (
                t.is_completed,
                PRIORITY_ORDER.get(t.priority, 2),
                -t.created_at.timestamp()
            )
        )

    # 5. ANNOTATE TASKS WITH COMPUTED PROPERTIES
    now_time = timezone.now()
    overdue_threshold  = timedelta(hours=24)
    stale_threshold    = timedelta(hours=12)
    warning_age_limit  = timedelta(hours=6)
    recent_threshold   = timedelta(minutes=15)
    detail_word_limit  = 6

    for task in tasks:
        # Strip archive flag for display clean text string
        display_title = task.title.replace(" [ARCHIVED]", "")
        clean = display_title.split('] ')[-1].strip() if ']' in display_title else display_title
        
        task.word_count   = len(clean.split())
        task.is_detailed  = task.word_count > detail_word_limit
        task.is_recent    = (now_time - task.created_at) < recent_threshold
        task.is_stale     = (now_time - task.created_at) > stale_threshold and not task.is_completed
        task.is_overdue   = (now_time - task.created_at) > overdue_threshold and not task.is_completed
        task.is_search_match = bool(search_query and search_query.lower() in task.title.lower())
        task.has_age_warning = (now_time - task.created_at) > warning_age_limit and not task.is_completed
        task.display_priority = task.priority.upper() if task.priority else "MED"
        task.title_char_length = len(clean)
        
        if task.word_count <= 2:
            task.density_label = "Quick"
        elif task.word_count <= 5:
            task.density_label = "Normal"
        else:
            task.density_label = "Complex"
        
        duration_match = re.search(r'(\d+)m\b', clean.lower())
        task.estimated_minutes = duration_match.group(1) if duration_match else None

    # 6. STATISTICS
    total_tasks         = Task.objects.exclude(title__icontains="[ARCHIVED]").count()
    completed_count     = Task.objects.filter(is_completed=True).exclude(title__icontains="[ARCHIVED]").count()
    total_pending_left  = Task.objects.filter(is_completed=False).exclude(title__icontains="[ARCHIVED]").count()
    high_pending_count  = Task.objects.filter(priority='high', is_completed=False).exclude(title__icontains="[ARCHIVED]").count()

    today = timezone.now().date()
    tasks_done_today    = Task.objects.filter(completed_at__date=today, is_completed=True).count()
    tasks_created_today = Task.objects.filter(created_at__date=today).count()

    completion_pct = round((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
    today_score    = f"{tasks_done_today}/{tasks_created_today}" if tasks_created_today > 0 else "0/0"
    critical_load  = high_pending_count >= 3

    today_pct = round((tasks_done_today / tasks_created_today) * 100) if tasks_created_today > 0 else 0
    if tasks_created_today == 0:
        today_level_status = "Clean Slate"
    elif today_pct == 100:
        today_level_status = "⭐ Elite Mode"
    elif today_pct >= 75:
        today_level_status = "⚡ Supercharged"
    elif today_pct >= 50:
        today_level_status = "📈 On Track"
    else:
        today_level_status = "🌱 Warming Up"

    milestone_celebration = ""
    if total_tasks > 0 and completion_pct == 100:
        milestone_celebration = "Perfect Day! All tasks are fully unlocked and closed. 🌟"
    elif total_tasks > 0 and completion_pct == 50:
        milestone_celebration = "Halfway point crossed! Great workflow consistency. 🎯"

    motivation_quote = get_motivation_quote(tasks_created_today, tasks_done_today, completion_pct)

    return render(request, 'tracker/index.html', {
        'tasks':               tasks,
        'dark_mode':           dark_mode,
        'today_score':         today_score,
        'completion_pct':      completion_pct,
        'total_tasks':         total_tasks,
        'search_query':        search_query,
        'filter_type':         filter_type,
        'sort_by':             sort_by,
        'selected_tag':        selected_tag,
        'view_archived':       view_archived,
        'now':                 timezone.now(),
        'high_pending_count':  high_pending_count,
        'critical_load':       critical_load,
        'motivation_quote':    motivation_quote,
        'total_pending_left':  total_pending_left,
        'current_list_count':  len(tasks),
        'milestone_celebration': milestone_celebration,
        'tag_emojis':          TAG_EMOJIS,
        'today_level_status':  today_level_status,
    })