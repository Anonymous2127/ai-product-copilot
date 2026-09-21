from typing import List

from pydantic import BaseModel, Field


class UserStory(BaseModel):
    role: str = Field(
        description="The user role"
    )

    goal: str = Field(
        description=(
            "What the user wants to achieve. "
            "Write it so it can naturally follow 'I want to'."
        )
    )

    benefit: str = Field(
        description=(
            "Why the user wants it. "
            "Write it so it can naturally follow 'so that'."
        )
    )


class ProductAnalysis(BaseModel):
    problem: str = Field(
        description="The core user problem"
    )

    target_users: List[str] = Field(
        description="Primary target users"
    )

    user_stories: List[UserStory] = Field(
        description="3 to 5 user stories"
    )

    mvp_features: List[str] = Field(
        description="Minimum features required for MVP"
    )

    acceptance_criteria: List[str] = Field(
        description="Testable acceptance criteria"
    )

    risks: List[str] = Field(
        description="Key product and AI risks"
    )

    assumptions: List[str] = Field(
        description="Assumptions that require validation"
    )

    open_questions: List[str] = Field(
        description="Questions requiring further research"
    )


class QualityIssue(BaseModel):
    category: str = Field(
        description=(
            "Issue category such as unsupported_metric, "
            "unsupported_assumption, scope_creep, "
            "unclear_requirement, or ai_risk"
        )
    )

    issue: str = Field(
        description="Description of the quality issue"
    )

    recommendation: str = Field(
        description="How the issue should be corrected"
    )


class QualityReview(BaseModel):
    passed: bool = Field(
        description=(
            "Whether the analysis passes quality review"
        )
    )

    issues: List[QualityIssue] = Field(
        description="Quality issues found in the analysis"
    )


class PRD(BaseModel):
    title: str = Field(
        description="Product or feature name"
    )

    executive_summary: str = Field(
        description=(
            "Short summary of the product opportunity"
        )
    )

    problem_statement: str = Field(
        description=(
            "The user problem the MVP intends to address"
        )
    )

    target_users: List[str] = Field(
        description="Target users for the MVP"
    )

    goals: List[str] = Field(
        description="Product goals"
    )

    non_goals: List[str] = Field(
        description=(
            "Capabilities explicitly excluded from the MVP"
        )
    )

    user_stories: List[str] = Field(
        description="Core MVP user stories"
    )

    mvp_scope: List[str] = Field(
        description="Features included in the MVP"
    )

    acceptance_criteria: List[str] = Field(
        description=(
            "Observable and testable acceptance criteria"
        )
    )

    risks: List[str] = Field(
        description=(
            "Product, AI, privacy, and technical risks"
        )
    )

    open_questions: List[str] = Field(
        description=(
            "Questions that still require validation"
        )
    )