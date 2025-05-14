"""pydantic Models for Quiz Generation and Analysis"""

from typing import List
from pydantic import BaseModel, Field


# ==============================
# MCQ-Question Generator Pydantic Models
# ==============================
class MCQQuestion(BaseModel):
    """Model for a single multiple-choice question."""

    question: str = Field(..., description="Clear, unambiguous question text")
    options: List[str] = Field(
        ...,
        min_items=4,
        max_items=4,
        description="List of answer options with exactly 4 items (1 correct, 3 distractors)",
    )
    correct_index: int = Field(
        ..., ge=0, le=3, description="Zero-based index of the correct answer (0-3)"
    )


class MCQQuiz(BaseModel):
    """Model for the complete quiz with multiple questions."""

    quiz: List[MCQQuestion] = Field(
        ..., min_items=5, max_items=5, description="Exactly 5 high-quality questions"
    )
    topic: str = Field(..., description="Main topic of the quiz derived from content")


# =============================
# Quiz Analysis Pydantic Models
# =============================
class QuizQuestionAnalysis(BaseModel):
    """Model for analyzing a single quiz question."""

    Question_Explanation: str = Field(
        ...,
        description="A brief summary of the question's focus and context, providing an overview of what the question is testing and its relevance to the source material.",
    )
    Answer_Feedback: str = Field(
        ...,
        description="Detailed explanations for each answer option, specifying whether it is correct or incorrect, with reasons and precise references to the source document (e.g., 'Section 2.1, Page 15').",
    )
    Correct_Answer: str = Field(
        ...,
        description="Identification of the correct answer with a clear justification, including a reference to the relevant section of the source document for accuracy.",
    )
    Related_Topics: str = Field(
        ...,
        description="A list of suggested topics for further study, tied to the content of the source document or broader related concepts to enhance learner understanding.",
    )


class QuizAnalysisOutput(BaseModel):
    """Model for the complete analysis of a quiz."""

    quiz: List[QuizQuestionAnalysis] = Field(
        ...,
        # description="A dictionary where keys are question identifiers (e.g., 'Q1', 'Q2') and values are QuizQuestionAnalysis objects containing the analysis for each quiz question."
    )


# =====================================
# TF-Question Generator Pydantic Models
# =====================================
class TrueFalseQuestion(BaseModel):
    """Model for a T-F question."""

    question: str = Field(..., title="The generated True/False question.")
    options: List[str] = Field(
        ...,
        min_items=2,
        max_items=2,
        description="List of answer options with exactly 2 items (1 correct, 1 distractor)",
    )
    correct_index: int = Field(
        ..., ge=0, le=1, description="Zero-based index of the correct answer (0-1)"
    )


class TrueFalseQuiz(BaseModel):
    """Model for the complete quiz with multiple questions."""

    quiz: List[TrueFalseQuestion] = Field(
        ...,
        min_items=5,
        max_items=5,
        description="Exactly 5 high-quality true/false questions",
    )
