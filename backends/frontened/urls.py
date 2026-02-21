from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='login'),
    path('courses/', TemplateView.as_view(template_name='courses.html'), name='courses'),
    path('assignments/', TemplateView.as_view(template_name='assignments.html'), name='assignments'),
]
