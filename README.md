
A# Daily Productivity Tracker 🚀

A simple and easy-to-use Daily Productivity Tracker built with Python and Django. This is my first Django project where I learned about basic CRUD operations, state management, and building clean web applications!

## 🌟 Features (Updated)
- **Add Tasks:** Quickly add new tasks to your daily to-do list.
- **Smart Auto-Tagging:** Automatically detects keywords (like 'code', 'study', 'meet', 'gym') to assign appropriate emojis and category tags instantly.
- **Priority Management:** Assign High, Medium, or Low priority to stay focused.
- **Smart Search:** Find specific tasks instantly with the built-in search bar.
- **Mark as Done:** Easily mark tasks as completed once finished.
- **Delete Tasks:** Remove unwanted or completed tasks permanently.
- **Dark Mode:** Eye-friendly interface for late-night study sessions.

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3 (Premium SaaS-style UI with DM Sans)
- **Database:** SQLite (Default Django DB)

## 📊 Development Process
This project was developed as a hands-on learning experience for:
- **Django Framework:** Implementing models, views, templates (MVT), and URL routing.
- **Frontend Integration:** Using Jinja2 syntax in templates for dynamic context rendering.
- **State Management:** Handling dark mode preferences and task filters dynamically through query parameters.
- **Data Integrity:** Constructing structural backend queries to carry out robust CRUD operations safely.

## ⚙️ How It Works (MVT Architecture)
This app strictly follows Django's Model-View-Template architecture:
1. **Model (`tracker/models.py`):** Defines the task schema (Title, Priority, Status, and Created Timestamp).
2. **View (`tracker/views.py`):** Processes incoming user requests, manages filtration (High, Pending, Completed), queries backend data, and injects context into templates.
3. **Template (`tracker/templates/`):** A responsive, premium frontend dashboard built to display state-driven dynamic elements natively.

## 📂 Project Structure
Here is a quick look at the core structure of this Django application:
```text
productivity_tracker/
│
├── healthcare_dashboard/     # Project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Core configurations (Dark Mode & Apps setup)
│   ├── urls.py               # Main project URL routing
│   └── wsgi.py               # WSGI server configuration
│
├── tracker/                  # Main Application directory
│   ├── migrations/           # Database migration tracker history
│   ├── models.py             # Task database model structure
│   ├── views.py              # Application controller logic (CRUD, Search, Filters)
│   └── templates/            # Frontend layout template files
│
├── manage.py                 # Django command-line execution manager
└── README.md                 # System project documentation

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