"""
View for listing and creating quizzes.

This file contains the view class for handling quiz listing and creation.
"""

from typing import Optional, Dict, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ...services.quiz_service import QuizService
from ..serializers.quiz_serializer import QuizSerializer


class QuizzesView(APIView):
    """
    View for listing and creating quizzes.
    This file contains the view class for handling quiz listing and creation.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor to inject QuizService into the view.
        """
        super().__init__(**kwargs)
        self.quiz_service: QuizService = QuizService()

    @extend_schema(
        responses={200: QuizSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="quiz_id", type="integer", required=False, description="Quiz ID"
            )
        ],
    )
    def get(self, quiz_id: Optional[int] = None) -> Response:
        """
        Retrieve all quizzes or a single quiz by ID.
        """
        if quiz_id:
            quiz: Dict[str, Any] = self.quiz_service.get_quiz_by_id(quiz_id)
            return Response(quiz, status=status.HTTP_200_OK)
        quizzes: list[Dict[str, Any]] = self.quiz_service.get_all_quizzes()
        return Response(quizzes, status=status.HTTP_200_OK)

    @extend_schema(request=QuizSerializer, responses={201: QuizSerializer})
    def post(self, request: Any) -> Response:
        """
        Create a new quiz.
        """
        quiz: Dict[str, Any] = self.quiz_service.create_quiz(request.data)
        return Response(quiz, status=status.HTTP_201_CREATED)

    @extend_schema(request=QuizSerializer, responses={200: QuizSerializer})
    def put(self, request: Any, quiz_id: int) -> Response:
        """
        Update an existing quiz.
        """
        quiz: Dict[str, Any] = self.quiz_service.update_quiz(quiz_id, request.data)
        return Response(quiz, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            204: OpenApiParameter(
                name="message", type="string", description="Quiz deleted successfully"
            )
        }
    )
    def delete(self, quiz_id: int) -> Response:
        """
        Delete a quiz by ID.
        """
        self.quiz_service.delete_quiz(quiz_id)
        return Response(
            {"message": "Quiz deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
