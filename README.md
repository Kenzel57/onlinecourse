# Online Course App — Django Final Project

A Django-based online learning platform with course enrollment, lesson delivery, and a multiple-choice exam engine with automatic grading.

---

## Features

- Browse and enroll in courses
- View lessons per course with Bootstrap-styled accordion layout
- Take multiple-choice exams after enrolling
- Automatic score calculation with pass/fail evaluation (≥ 80% to pass)
- Django admin panel for managing courses, lessons, questions, choices, and submissions

---

## Project Structure

```
onlinecourse/                  ← GitHub repository root
├── manage.py
├── README.md
├── requirements.txt
├── mysite/                    ← Django project package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── onlinecourse/              ← Django app
    ├── models.py              ← Task 1: Question, Choice, Submission models
    ├── admin.py               ← Task 2: QuestionInline, ChoiceInline, QuestionAdmin, LessonAdmin
    ├── views.py               ← Task 5: submit() and show_exam_result() views
    ├── urls.py                ← Task 6: /submit/ and /submission/<id>/result/ paths
    ├── migrations/
    └── templates/
        └── onlinecourse/
            ├── course_details_bootstrap.html   ← Task 4: course detail + exam form
            └── exam_result_bootstrap.html      ← Task 7: score + congratulations page
```

---

## Models

### Pre-existing
| Model | Description |
|---|---|
| `Instructor` | Linked to Django `User`; marks full-time status |
| `Learner` | Linked to Django `User`; stores occupation and social link |
| `Course` | Name, image, description, instructors, enrolled users |
| `Lesson` | Title, order, content; FK to `Course` |
| `Enrollment` | M2M bridge between `User` and `Course`; stores mode and rating |

### Added in final project
| Model | Description |
|---|---|
| `Question` | Exam question with `grade` (points); FK to `Course`. Has `is_get_score(selected_ids)` helper |
| `Choice` | Possible answer with `is_correct` flag; FK to `Question` |
| `Submission` | Records a learner's attempt; FK to `Enrollment`, M2M to `Choice` |

---

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/<your-username>/onlinecourse.git
cd onlinecourse

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

Then open [http://127.0.0.1:8000/onlinecourse/](http://127.0.0.1:8000/onlinecourse/) in your browser.

---

## URL Routes

| URL | View | Name |
|---|---|---|
| `/onlinecourse/` | `index` | `onlinecourse:index` |
| `/onlinecourse/<id>/` | `detail` | `onlinecourse:detail` |
| `/onlinecourse/<id>/enroll/` | `enroll` | `onlinecourse:enroll` |
| `/onlinecourse/<id>/submit/` | `submit` | `onlinecourse:submit` |
| `/onlinecourse/<id>/submission/<sub_id>/result/` | `show_exam_result` | `onlinecourse:show_exam_result` |
| `/admin/` | Django admin | — |

---

## Admin Panel

Visit `/admin/` and log in with your superuser credentials to manage:

- **Authentication and Authorization** — Users, Groups
- **Onlinecourse** — Courses (with inline Questions), Lessons, Questions (with inline Choices), Choices, Enrollments, Instructors, Learners, Submissions

---

## Exam Logic

1. An enrolled learner opens the course detail page and sees the exam form.
2. They select one or more choices per question and click **Submit Exam**.
3. The `submit` view creates a `Submission` record and attaches all selected `Choice` objects.
4. The learner is redirected to the result page rendered by `show_exam_result`.
5. Each question is scored using `question.is_get_score(selected_ids)` — the learner must select **all** correct choices and **no** incorrect ones to earn the question's points.
6. A total score ≥ 80% displays the **Congratulations** message.

---

## Requirements

```
Django>=4.2
Pillow>=10.0
```

---

## License

This project was built as part of the IBM Full Stack Software Developer Professional Certificate on Coursera.
