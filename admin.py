from django.contrib import admin

# Task 2 — 7 imported classes
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


# -----------------------------------------------------------------
# Inline classes
# -----------------------------------------------------------------

class ChoiceInline(admin.StackedInline):
    """Allows Choices to be edited inline within the Question admin page."""
    model = Choice
    extra = 4            # display 4 blank choice forms by default


class QuestionInline(admin.StackedInline):
    """Allows Questions to be added inline within the Course admin page."""
    model = Question
    extra = 5            # display 5 blank question forms by default


# -----------------------------------------------------------------
# ModelAdmin classes
# -----------------------------------------------------------------

class QuestionAdmin(admin.ModelAdmin):
    """Admin view for Questions, with Choices nested inside."""
    inlines = [ChoiceInline]
    list_display = ['content', 'course', 'grade']
    list_filter  = ['course']
    search_fields = ['content']


class LessonAdmin(admin.ModelAdmin):
    """Admin view for Lessons."""
    list_display = ['title', 'order', 'course']
    list_filter  = ['course']
    search_fields = ['title']


# -----------------------------------------------------------------
# CourseAdmin with QuestionInline
# -----------------------------------------------------------------

class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['name', 'pub_date', 'total_enrollment']
    search_fields = ['name', 'description']


# -----------------------------------------------------------------
# Register all models
# -----------------------------------------------------------------

admin.site.register(Course,      CourseAdmin)
admin.site.register(Lesson,      LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question,    QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
