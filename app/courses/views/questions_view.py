"""
View for managing questions using the QuestionService.
Provides endpoints for retrieving, creating, updating, and deleting questions.
"""

from typing import Optional, Any
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from ...services.question_service import QuestionService

class QuestionsView(APIView):
    """
    View for managing questions using the QuestionService.
    Provides endpoints for retrieving, creating, updating, and deleting questions.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Constructor to inject QuestionService into the view.
        """
        super().__init__(**kwargs)
        self.question_service: QuestionService = QuestionService()

    def get(self, _request: Request, quiz_id: Optional[int] = None) -> Response:
        """
        Retrieve all questions for a given quiz.
        """
        if not quiz_id:
            return self._error_response("quiz_id is required to retrieve questions.")
        questions = self.question_service.get_all_questions(quiz_id)
        return Response(questions, status=status.HTTP_200_OK)

    def post(self, request: Request, quiz_id: Optional[int] = None) -> Response:
        """
        Create a new question for a given quiz.
        """
        if not quiz_id:
            return self._error_response("quiz_id is required to create a question.")
        question = self.question_service.create_question(quiz_id, request.data)
        return Response(question, status=status.HTTP_201_CREATED)

    def put(self, request: Request, question_id: Optional[int] = None) -> Response:
        """
        Update an existing question by its ID.
        """
        if not question_id:
            return self._error_response("question_id is required to update a question.")
        question = self.question_service.update_question(question_id, request.data)
        return Response(question, status=status.HTTP_200_OK)

    def delete(self, _request: Request, question_id: Optional[int] = None) -> Response:
        """
        Delete a question by its ID.
        """
        if not question_id:
            return self._error_response("question_id is required to delete a question.")
        self.question_service.delete_question(question_id)
        return Response(
            {"message": "Question deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    def _error_response(self,
        message: str,
        http_status: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """
        Helper method to return a consistent error response with a given message and status.
        """
        return Response({"error": message}, status=http_status)
