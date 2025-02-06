"""
View for listing and creating quizzes.

This file contains the view class for handling quiz listing and creation.
"""

from typing import Optional, Dict, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...services.quiz_service import QuizService


class QuizzesView(APIView):
    """
    View for managing quizzes using QuizService.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor to inject QuizService into the view.
        """
        super().__init__(**kwargs)
        self.quiz_service: QuizService = QuizService()

    def get(self, quiz_id: Optional[int] = None) -> Response:
        """
        Retrieve all quizzes or a single quiz by ID.
        """
        if quiz_id:
            quiz: Dict[str, Any] = self.quiz_service.get_quiz_by_id(quiz_id)
            return Response(quiz, status=status.HTTP_200_OK)
        quizzes: list[Dict[str, Any]] = self.quiz_service.get_all_quizzes()
        return Response(quizzes, status=status.HTTP_200_OK)

    def post(self, request: Any) -> Response:
        """
        Create a new quiz.
        """
        quiz: Dict[str, Any] = self.quiz_service.create_quiz(request.data)
        return Response(quiz, status=status.HTTP_201_CREATED)

    def put(self, request: Any, quiz_id: int) -> Response:
        """
        Update an existing quiz.
        """
        quiz: Dict[str, Any] = self.quiz_service.update_quiz(quiz_id, request.data)
        return Response(quiz, status=status.HTTP_200_OK)

    def delete(self, quiz_id: int) -> Response:
        """
        Delete a quiz by ID.
        """
        self.quiz_service.delete_quiz(quiz_id)
        return Response(
            {"message": "Quiz deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
