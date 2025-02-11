"""
Service for managing answers.

This is a service class to handle actions related to answers.
"""

from typing import Any, Dict, List
from django.shortcuts import get_object_or_404
from ..courses.models.answer_model import AnswerModel
from ..courses.models.question_model import QuestionModel
from ..courses.serializers.answer_serializer import AnswerSerializer


class AnswerService:
    """
    Service class for handling Answer-related operations.
    """

    def get_answer_by_id(self, answer_id: int) -> Dict[str, Any]:
        """
        Retrieve an answer by its ID and serialize it.

        :param answer_id: ID of the answer to retrieve.
        :return: Serialized answer data as a dictionary.
        """
        answer: AnswerModel = get_object_or_404(AnswerModel, id=answer_id)
        serializer: AnswerSerializer = AnswerSerializer(answer)
        return serializer.data

    def get_all_answers(self, question_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all answers associated with a question.

        :param question_id: ID of the question.
        :return: List of serialized answer data.
        """
        question: QuestionModel = get_object_or_404(QuestionModel, id=question_id)
        answers = AnswerModel.objects.filter(  # pylint: disable=no-member
            question=question
        )  # pylint: disable=no-member
        serializer: AnswerSerializer = AnswerSerializer(answers, many=True)
        return serializer.data

    def get_answers_by_question(self, question_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all answers associated with a question, using the question ID.

        :param question_id: ID of the question to retrieve answers for.
        :return: List of serialized answer data.
        """
        # Retrieve the question to ensure it exists
        question: QuestionModel = get_object_or_404(QuestionModel, id=question_id)

        # Fetch answers associated with the given question
        answers = AnswerModel.objects.filter(  # pylint: disable=no-member
            question=question
        )  # pylint: disable=no-member
        # Serialize the answer data and return
        serializer: AnswerSerializer = AnswerSerializer(answers, many=True)
        return serializer.data

    def create_answer(self, question_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new answer for a specific question.

        :param question_id: ID of the question.
        :param data: Dictionary containing answer data.
        :return: Serialized answer data.
        """
        # Ensure the question exists
        question: QuestionModel = get_object_or_404(QuestionModel, id=question_id)

        # Attach the question ID to the answer data
        data["question"] = question.id

        # Validate and save the answer
        serializer: AnswerSerializer = AnswerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update_answer(self, answer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing answer.

        :param answer_id: ID of the answer to update.
        :param data: Dictionary containing updated answer data.
        :return: Serialized updated answer data.
        """
        answer: AnswerModel = get_object_or_404(AnswerModel, id=answer_id)
        serializer: AnswerSerializer = AnswerSerializer(answer, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_answer(self, answer_id: int) -> None:
        """
        Delete an answer by its ID.

        :param answer_id: ID of the answer to delete.
        """
        answer: AnswerModel = get_object_or_404(AnswerModel, id=answer_id)
        answer.delete()

    def delete_answer_by_question_and_text(
        self, question_id: int, answer_text: str
    ) -> None:
        """
        Delete an answer by its text for a specific question.

        :param question_id: ID of the question to delete the answer from.
        :param answer_text: The text of the answer to delete.
        :return: None
        """
        # Ensure the answer_text variable is passed when calling this method
        # Filter answers by the question and the text
        answer = AnswerModel.objects.filter(  # pylint: disable=no-member
            question_id=question_id, text=answer_text
        ).first()

        if answer:
            answer.delete()
        else:
            raise ValueError(
                f"Answer with text '{answer_text}' not found for question {question_id}."
            )

    def delete_answers_by_question(self, question_id: int) -> None:
        """
        Delete all answers for a given question.

        :param question_id: ID of the question whose answers should be deleted.
        """
        deleted_count, _ = AnswerModel.objects.filter(  # pylint: disable=no-member
            question_id=question_id
        ).delete()  # pylint: disable=no-member

        if deleted_count == 0:
            raise ValueError(f"No answers found for question {question_id}.")
