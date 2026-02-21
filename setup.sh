#!/bin/bash
# Mini LMS Setup Script
echo "🎓 Setting up Mini LMS..."

cd backend

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r ../requirements.txt

# Run migrations
echo "🗃️ Running migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py migrate

# Create superuser
echo "👤 Creating demo users..."
python manage.py shell << 'EOF'
from accounts.models import User

# Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@lms.com', 'admin123', role='admin')
    print("  ✅ Admin: admin / admin123")

# Instructor
if not User.objects.filter(username='instructor').exists():
    u = User.objects.create_user('instructor', 'instructor@lms.com', 'pass123', role='instructor',
                                  first_name='Jane', last_name='Smith')
    print("  ✅ Instructor: instructor / pass123")

# Student
if not User.objects.filter(username='student').exists():
    u = User.objects.create_user('student', 'student@lms.com', 'pass123', role='student',
                                  first_name='John', last_name='Doe')
    print("  ✅ Student: student / pass123")

# Create sample course
from courses.models import Course, Lesson, Assignment
from django.utils import timezone
from datetime import timedelta

instructor = User.objects.get(username='instructor')
student = User.objects.get(username='student')

if not Course.objects.exists():
    course = Course.objects.create(
        title='Introduction to Python',
        description='Learn Python programming from scratch. Cover variables, loops, functions, OOP, and more.',
        instructor=instructor
    )
    course.students.add(student)

    Lesson.objects.create(course=course, title='Python Basics', content='Variables, data types, and operators in Python.', order=1)
    Lesson.objects.create(course=course, title='Control Flow', content='If statements, loops, and functions.', order=2)
    Lesson.objects.create(course=course, title='OOP in Python', content='Classes, objects, inheritance.', order=3)

    Assignment.objects.create(
        course=course,
        title='Hello World Project',
        description='Write a Python script that prints "Hello, World!" and ask the user their name.',
        due_date=timezone.now() + timedelta(days=7),
        max_score=100
    )
    print("  ✅ Sample course + lessons + assignment created")

print("\n🎉 Demo data ready!")
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting server..."
echo "   Open: http://localhost:8000"
echo ""
python manage.py runserver
