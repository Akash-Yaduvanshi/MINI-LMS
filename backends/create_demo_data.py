import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Lesson, Assignment
from django.utils import timezone
from datetime import timedelta

def create_demo_data():
    print("👤 Creating demo users...")

    # Admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@lms.com', 'admin123', role='admin')
        print("  ✅ Admin: admin / admin123")
    else:
        print("  ℹ️ Admin already exists")

    # Instructor
    if not User.objects.filter(username='instructor').exists():
        User.objects.create_user('instructor', 'instructor@lms.com', 'pass123', role='instructor',
                                      first_name='Jane', last_name='Smith')
        print("  ✅ Instructor: instructor / pass123")
    else:
        print("  ℹ️ Instructor already exists")

    # Student
    if not User.objects.filter(username='student').exists():
        User.objects.create_user('student', 'student@lms.com', 'pass123', role='student',
                                      first_name='John', last_name='Doe')
        print("  ✅ Student: student / pass123")
    else:
        print("  ℹ️ Student already exists")

    # Create sample course
    try:
        instructor = User.objects.get(username='instructor')
        student = User.objects.get(username='student')

        if not Course.objects.exists():
            print("📚 Creating sample course...")
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
        else:
            print("  ℹ️ Courses already exist")

    except User.DoesNotExist:
        print("  ❌ Error: Instructor or Student user not found. Cannot create course.")

    print("\n🎉 Demo data ready!")

if __name__ == '__main__':
    create_demo_data()
