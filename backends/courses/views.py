from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Assignment, Submission
from .serializers import (
    CourseSerializer, CourseCreateSerializer,
    LessonSerializer, AssignmentSerializer, SubmissionSerializer
)
from .permissions import IsInstructor, IsInstructorOrReadOnly


class CourseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Course.objects.filter(instructor=user)
        return Course.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsInstructorOrReadOnly]
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CourseCreateSerializer
        return CourseSerializer


class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk, is_published=True)
        if request.user.role != 'student':
            return Response({'error': 'Only students can enroll.'}, status=status.HTTP_403_FORBIDDEN)
        course.students.add(request.user)
        return Response({'message': f'Enrolled in {course.title} successfully.'})

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.students.remove(request.user)
        return Response({'message': 'Unenrolled successfully.'})


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])

    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        serializer.save(course=course)


class AssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return Assignment.objects.filter(course__instructor=user)
        return Assignment.objects.filter(course__students=user)

    def perform_create(self, serializer):
        if self.request.user.role not in ('instructor', 'admin'):
            raise permissions.PermissionDenied("Only instructors can create assignments.")
        serializer.save()


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsInstructorOrReadOnly]
    queryset = Assignment.objects.all()


class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Submission.objects.filter(student=user)
        elif user.role == 'instructor':
            return Submission.objects.filter(assignment__course__instructor=user)
        return Submission.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Submission.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Only instructor can grade
        if 'score' in request.data or 'feedback' in request.data:
            if request.user.role not in ('instructor', 'admin'):
                return Response({'error': 'Only instructors can grade submissions.'}, status=403)
            data = {
                'score': request.data.get('score', instance.score),
                'feedback': request.data.get('feedback', instance.feedback),
                'status': 'graded'
            }
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(**data)
            return Response(serializer.data)
        return super().update(request, *args, **kwargs)
