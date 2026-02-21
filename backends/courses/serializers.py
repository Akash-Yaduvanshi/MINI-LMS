from rest_framework import serializers
from .models import Course, Lesson, Assignment, Submission
from accounts.serializers import UserSerializer


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'order', 'created_at')
        read_only_fields = ('id', 'created_at')


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    student_count = serializers.ReadOnlyField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'instructor', 'lessons',
                  'student_count', 'is_enrolled', 'is_published', 'created_at')
        read_only_fields = ('id', 'instructor', 'created_at')

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.students.filter(id=request.user.id).exists()
        return False


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'is_published')
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class AssignmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    submission_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ('id', 'course', 'course_title', 'title', 'description',
                  'due_date', 'max_score', 'submission_count', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_submission_count(self, obj):
        return obj.submissions.count()


class SubmissionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Submission
        fields = ('id', 'assignment', 'assignment_title', 'student', 'content',
                  'score', 'feedback', 'status', 'submitted_at')
        read_only_fields = ('id', 'student', 'submitted_at', 'score', 'feedback', 'status')

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)
