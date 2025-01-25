"""
URL configuration for the courses.
"""

from django.urls import path
from ..courses.views.courses_view import CoursesView
from ..courses.views.quizzes_view import QuizzesView
from ..courses.views.questions_view import QuestionsView

urlpatterns = [
    path('', CoursesView.as_view(), name='courses-list'),
    path('<int:course_id>/', CoursesView.as_view(), name='course-detail'),
    path('<int:course_id>/quizzes/', QuizzesView.as_view(), name='quizzes-list'),
    path('quizzes/<int:quiz_id>/questions/', QuestionsView.as_view(), name='questions-list'),
    path('quizzes/<int:quiz_id>/questions/<int:question_id>/',
         QuestionsView.as_view(),
         name='question-detail'
    ),
]
