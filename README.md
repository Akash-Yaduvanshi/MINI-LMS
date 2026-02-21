# 🎓 Mini LMS - Learning Management System

A full-stack Learning Management System built with Django REST Framework + JWT Authentication + HTML/CSS frontend.

---

## 🚀 Quick Start

```bash
# 1. Clone / extract project
cd mini_lms

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Run setup (installs packages, runs migrations, creates demo users)
bash setup.sh
```

Open **http://localhost:8000** in your browser.

---

## 🔑 Demo Credentials

| Role       | Username   | Password  |
|------------|------------|-----------|
| Admin      | admin      | admin123  |
| Instructor | instructor | pass123   |
| Student    | student    | pass123   |

---

## 📁 Project Structure

```
mini_lms/
├── requirements.txt
├── setup.sh
└── backend/
    ├── manage.py
    ├── backend/          # Django settings & URLs
    ├── accounts/         # Users, registration, JWT auth
    ├── courses/          # Courses, lessons, assignments, submissions
    └── frontend/
        ├── templates/    # HTML pages
        │   ├── index.html        # Login / Register
        │   ├── courses.html      # Course management
        │   └── assignments.html  # Assignment submission & grading
        └── static/
            └── style.css  # All styles
```

---

## 🌐 Pages

| URL            | Description                        |
|----------------|------------------------------------|
| `/`            | Login / Register page              |
| `/courses/`    | Course listing, enrollment, lessons|
| `/assignments/`| Assignment submission & grading    |
| `/admin/`      | Django admin panel                 |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint                    | Description          |
|--------|-----------------------------|----------------------|
| POST   | `/api/token/`               | Login (get JWT)      |
| POST   | `/api/token/refresh/`       | Refresh token        |
| POST   | `/api/accounts/register/`   | Register new user    |
| GET    | `/api/accounts/profile/`    | Get current user     |

### Courses
| Method | Endpoint                         | Description           |
|--------|----------------------------------|-----------------------|
| GET    | `/api/courses/`                  | List courses          |
| POST   | `/api/courses/`                  | Create course         |
| GET    | `/api/courses/<id>/`             | Course detail         |
| POST   | `/api/courses/<id>/enroll/`      | Enroll in course      |
| DELETE | `/api/courses/<id>/enroll/`      | Unenroll from course  |
| GET    | `/api/courses/<id>/lessons/`     | List lessons          |
| POST   | `/api/courses/<id>/lessons/`     | Add lesson            |

### Assignments & Submissions
| Method | Endpoint                            | Description            |
|--------|-------------------------------------|------------------------|
| GET    | `/api/courses/assignments/`         | List assignments       |
| POST   | `/api/courses/assignments/`         | Create assignment      |
| GET    | `/api/courses/submissions/`         | List submissions       |
| POST   | `/api/courses/submissions/`         | Submit assignment      |
| PATCH  | `/api/courses/submissions/<id>/`    | Grade submission       |

---

## 🎭 Role Permissions

| Feature              | Admin | Instructor | Student |
|----------------------|-------|------------|---------|
| Create courses       | ✅    | ✅         | ❌      |
| Add lessons          | ✅    | ✅         | ❌      |
| Create assignments   | ✅    | ✅         | ❌      |
| Enroll in courses    | ❌    | ❌         | ✅      |
| Submit assignments   | ❌    | ❌         | ✅      |
| Grade submissions    | ✅    | ✅         | ❌      |
| View all users       | ✅    | ❌         | ❌      |

---

## 🔧 Tech Stack

- **Backend**: Python, Django 4.2, Django REST Framework
- **Auth**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (dev) — swap for PostgreSQL in production
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **CORS**: django-cors-headers

---

## 🚀 Future Improvements

- [ ] File upload for assignments
- [ ] Grading analytics dashboard
- [ ] Email notifications
- [ ] Video lesson support
- [ ] Payment integration (Stripe)
- [ ] Deploy to Railway / Render / AWS
