# Daily Productivity Tracker 🚀

A simple, premium, and feature-rich Daily Productivity Tracker built with Python and Django. This project showcases structured CRUD operations, dynamic state management, automated data transformation, and custom SaaS-style minimalist UI dashboard design.

## 🌐 Features (Updated & Advanced)
- **Add Tasks:** Quickly add new tasks to your daily to-do list.
- **Smart Auto-Tagging:** Automatically detects keywords (like 'code', 'study', 'meet', 'gym') to assign appropriate emojis and category tags instantly.
- **Priority Management:** Assign High, Medium, or Low priority to stay focused with color-coded structural left borders.
- **Interactive Tasks Shortcuts Toolbar:** Filter your dashboard view dynamically by departments (💻 Work, 📚 Study, 🤝 Meet, etc.) with a single click.
- **Dual-Mode Sorting Switch:** Toggle your workspace view instantly between **Default Smart Sort** (Incomplete first + Priority) and **Latest First** viewports.
- **Smart Focus Duration Parser:** Built-in regex engine automatically extracts time frames (e.g., `45m`, `60m`) from titles to display standalone ⏳ focus badges.
- **Task Word-Density Progression Labels:** Dynamically analyzes word lengths on the backend to flag cards as `Quick`, `Normal`, or `Complex` structures.
- **Real-time Metrics & Character Counter:** Processes runtime string lengths directly from the backend controller to map precise character metrics onto active items.
- **Live Productivity Score Health Badge:** Evaluates your daily task execution rates to badge your score panel dynamically with tags like `⭐ Elite Mode`, `⚡ Supercharged`, or `📈 On Track`.
- **High-Urgency Visual Alert Engine:** Flags critical loads when high-priority items spike, and injects custom soft red outline glows for overdue items (older than 24h).
- **Wipe Out Utility Engine:** Includes a safe confirmation modal wrapper to completely clear individual items, clear completed tasks, or wipe the entire database clean.
- **Dark Mode Wrapper:** Seamless session-based light and dark mode preferences toggle for late-night programming sessions.

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3 Variables (Premium minimalist design with custom typefaces: *Syne*, *Lato*, *JetBrains Mono*)
- **Database:** SQLite (Default Django DB)

## 📊 Development Process
This project was developed as a hands-on learning experience for:
- **Django Core Framework:** Implementing models, views, templates (MVT), flash messaging frameworks, and session controls.
- **Frontend Integration:** Using Jinja2 template tagging expressions for dynamic contextual loops and multi-tier styling conditions natively.
- **State Management:** Handling theme preferences, tag selections, sorting states, and multi-stage filters dynamically via clean query parameters.
- **Data Integrity:** Constructing structural Python backend logic to process robust CRUD operations safely.

## ⚙️ How It Works (MVT Architecture)
This app strictly follows Django's Model-View-Template architecture:
1. **Model (`tracker/models.py`):** Defines the task database schema (Title, Priority, Completion Status, and Created/Completed Timestamps).
2. **View (`tracker/views.py`):** Processes user requests, coordinates multi-tier parsing loops, updates records, maps calculated attributes, and injects context blocks into the frontend layer.
3. **Template (`tracker/templates/`):** A responsive, fluid, micro-interaction-focused dashboard template built to render variable backend properties natively.

## 📂 Project Structure
Here is a quick look at the core structure of this Django application:
```text
productivity_tracker/
│
├── healthcare_dashboard/     # Project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Core configurations (WSGI, WhiteNoise & Production flags)
│   ├── urls.py               # Main project URL routing mappings
│   └── wsgi.py               # WSGI application entry-point for web servers
│
├── tracker/                  # Main Application directory
│   ├── migrations/           # Database schema migration tracking records
│   ├── models.py             # Task database model layout
│   ├── views.py              # Controller core architecture (CRUD handlers, RegEx parsers, Filters)
│   └── templates/            # Minimalist dashboard frontend layouts
│
├── manage.py                 # Django command-line execution utility manager
├── requirements.txt          # Python dependency packages map frozen for live servers
└── README.md                 # System project documentation & developer logs

## 📝 Future Scope
- User Authentication for multiple accounts.
- Integration of a Data Science dashboard to track productivity trends over time.
- Adding deadlines and push notifications.

## 🚀 How to Run Locally
If you want to run this project on your computer, follow these steps:

1. Clone this repository:
   ```bash
   git clone [https://github.com/Manyatagupta/productivity_tracker.git](https://github.com/Manyatagupta/productivity_tracker.git)

2. Open the folder and create a virtual environment.

3. Install Django: 
   pip install django


4. Run the server: 
   python manage.py runserver