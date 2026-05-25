from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Course, Enrollment, Question, Choice, Submission


def get_enrollment_or_redirect(request, course_id):
    """Helper — return the Enrollment for the current user, or raise 404."""
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    return course, enrollment


# -----------------------------------------------------------------------
# Existing views (kept for reference — adapt to your existing code)
# -----------------------------------------------------------------------

def index(request):
    """List all available courses."""
    courses = Course.objects.all()
    return render(request, 'onlinecourse/index.html', {'course_list': courses})


def detail(request, course_id):
    """Course detail page with lessons and exam."""
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_authenticated:
        try:
            Enrollment.objects.get(user=request.user, course=course)
            course.is_enrolled = True
        except Enrollment.DoesNotExist:
            course.is_enrolled = False
    context['course'] = course
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    try:
        Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse('onlinecourse:detail', args=(course.id,)))


# -----------------------------------------------------------------------
# Task 5 — NEW VIEWS: submit & show_exam_result
# -----------------------------------------------------------------------

@login_required
def submit(request, course_id):
    """
    Handle exam submission:
    1. Retrieve the user's enrollment for this course.
    2. Create a new Submission linked to that enrollment.
    3. Collect all selected choice IDs from the POST data.
    4. Add each Choice to the Submission.
    5. Redirect to the exam result page.
    """
    course, enrollment = get_enrollment_or_redirect(request, course_id)

    # Create a fresh submission for this attempt
    submission = Submission.objects.create(enrollment=enrollment)

    # Collect submitted choice ids (multiple checkboxes named 'choice')
    submitted_choice_ids = request.POST.getlist('choice')
    for choice_id in submitted_choice_ids:
        choice = get_object_or_404(Choice, pk=choice_id)
        submission.choices.add(choice)

    submission.save()

    return HttpResponseRedirect(
        reverse('onlinecourse:show_exam_result', args=(course_id, submission.id))
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Display exam results:
    - Show each question with the learner's selected choices highlighted.
    - Calculate total score earned vs. total possible score.
    - Display 'Congratulations' message if the learner passed (>= 80 %).
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # IDs of choices the user submitted
    selected_ids = submission.choices.values_list('id', flat=True)

    # Calculate score
    total_score = 0.0
    earned_score = 0.0

    questions = course.question_set.all()
    for question in questions:
        total_score += question.grade
        if question.is_get_score(selected_ids):
            earned_score += question.grade

    # Determine pass/fail (pass threshold: 80 %)
    passed = (earned_score / total_score >= 0.80) if total_score > 0 else False

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'questions': questions,
        'total_score': total_score,
        'earned_score': earned_score,
        'passed': passed,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
