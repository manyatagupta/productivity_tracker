# Daily Productivity Tracker 🚀

A simple and easy-to-use Daily Productivity Tracker built with Python and Django. This is my first Django project where I learned about basic CRUD operations!

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
- **Frontend:** HTML, CSS (Premium SaaS-style UI with DM Sans)
- **Database:** SQLite (Default Django DB)

## 📊 Development Process
This project was developed as a hands-on learning experience for:
- **Django Framework:** Implementing models, views, and URL routing.
- **Frontend Integration:** Using Jinja2 templates for dynamic content.
- **State Management:** Handling dark mode and task status through query parameters.
- **Data Integrity:** Basic CRUD operations with a focus on clean logic.

## 📂 Project Structure
Here is a quick look at the core structure of this Django application:
```text
productivity_tracker/
│
├── healthcare_dashboard/     # Project configuration directory
│   ├── __init__.py
│   ├── settings.py           # Core settings (Dark Mode & Apps setup)
│   ├── urls.py               # Main URL routing
│   └── wsgi.py
│
├── tracker/                  # Main Application directory
│   ├── migrations/           # Database migration files
│   ├── models.py             # Task model (Title, Priority, Status)
│   ├── views.py              # Main logic for CRUD, Search, and Filters
│   └── templates/            # HTML files (Premium template)
│
├── manage.py                 # Django command-line utility
└── README.md                 # Project documentation

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