from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Home — list all courses
    path('', views.index, name='index'),

    # Course detail page
    path('<int:course_id>/', views.detail, name='detail'),

    # Enroll in a course
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Task 6 — NEW URL paths
    # Submit exam answers → creates a Submission and redirects to results
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Show exam result for a specific submission
    path('<int:course_id>/submission/<int:submission_id>/result/',
         views.show_exam_result,
         name='show_exam_result'),
]
