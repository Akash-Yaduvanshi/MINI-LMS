from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, EnrollView,
    LessonListCreateView,
    AssignmentListCreateView, AssignmentDetailView,
    SubmissionListCreateView, SubmissionDetailView,
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:pk>/enroll/', EnrollView.as_view(), name='course-enroll'),
    path('<int:course_pk>/lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment-list'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
]
