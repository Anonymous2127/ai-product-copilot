from langchain_core.prompts import ChatPromptTemplate

from src.llm import get_llm

from src.prompts import (
    SYSTEM_PROMPT,
    ANALYSIS_PROMPT,
    REVIEW_PROMPT,
    PRD_PROMPT,
)

from src.schemas import (
    ProductAnalysis,
    QualityReview,
    PRD,
)


def analyze_requirement(
    requirement: str,
) -> ProductAnalysis:

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        ProductAnalysis
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            (
                "human",
                ANALYSIS_PROMPT,
            ),
        ]
    )

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "requirement": requirement,
        }
    )

    return result


def review_analysis(
    requirement: str,
    analysis: ProductAnalysis,
) -> QualityReview:

    llm = get_llm()

    reviewer = llm.with_structured_output(
        QualityReview
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a rigorous AI product "
                    "quality reviewer."
                ),
            ),
            (
                "human",
                REVIEW_PROMPT,
            ),
        ]
    )

    chain = prompt | reviewer

    review = chain.invoke(
        {
            "requirement": requirement,
            "analysis": analysis.model_dump_json(
                indent=2
            ),
        }
    )

    return review


def generate_prd(
    requirement: str,
    analysis: ProductAnalysis,
    review: QualityReview,
    human_instructions: str,
) -> PRD:

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        PRD
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are an experienced AI "
                    "product manager."
                ),
            ),
            (
                "human",
                PRD_PROMPT,
            ),
        ]
    )

    chain = prompt | structured_llm

    prd = chain.invoke(
        {
            "requirement": requirement,
            "analysis": analysis.model_dump_json(
                indent=2
            ),
            "review": review.model_dump_json(
                indent=2
            ),
            "human_instructions": (
                human_instructions
                if human_instructions.strip()
                else (
                    "No additional human instructions "
                    "were provided."
                )
            ),
        }
    )

    return prd