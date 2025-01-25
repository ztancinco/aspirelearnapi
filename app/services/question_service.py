"""
Service for managing questions.

This is a service class to handle actions related to questions.
"""

from django.shortcuts import get_object_or_404
from ..courses.models.quiz_model import QuizModel
from ..courses.models.question_model import QuestionModel
from ..courses.serializers.question_serializer import QuestionSerializer

class QuestionService:
    """
    Service class for handling Question-related operations.
    """

    def get_question_by_id(self, question_id):
        """
        Retrieve a question by its ID and serialize it.

        :param question_id: ID of the question to retrieve
        :return: Serialized question data
        """
        question = get_object_or_404(QuestionModel, id=question_id)
        serializer = QuestionSerializer(question)
        return serializer.data

    def get_all_questions(self, quiz_id):
        """
        Retrieve all questions associated with a quiz.

        :param quiz_id: ID of the quiz
        :return: Serialized list of questions
        """
        quiz = get_object_or_404(QuizModel, id=quiz_id)
        questions = QuestionModel.objects.filter(quiz=quiz)  # pylint: disable=no-member
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data

    def create_question(self, quiz_id, data):
        """
        Create a new question for a specific quiz.

        :param quiz_id: ID of the quiz
        :param data: Dictionary containing question data
        :return: Serialized question data
        """
        # Ensure the quiz exists
        quiz = get_object_or_404(QuizModel, id=quiz_id)

        # Attach the quiz ID to the question data
        data['quiz'] = quiz.id

        # Validate and save the question
        serializer = QuestionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update_question(self, question_id, data):
        """
        Update an existing question.

        :param question_id: ID of the question to update
        :param data: Dictionary containing updated question data
        :return: Serialized updated question data
        """
        question = get_object_or_404(QuestionModel, id=question_id)
        serializer = QuestionSerializer(question, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_question(self, question_id):
        """
        Delete a question by its ID.

        :param question_id: ID of the question to delete
        """
        question = get_object_or_404(QuestionModel, id=question_id)
        question.delete()
