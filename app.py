import streamlit as st

from src.workflow import (
    analyze_requirement,
    review_analysis,
    generate_prd,
)


# =========================================================
# Page Config
# =========================================================

st.set_page_config(
    page_title="AI Product Copilot",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main page width */
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Reduce default Streamlit top whitespace */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Hero */
    .hero-label {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        opacity: 0.65;
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 750;
        line-height: 1.05;
        letter-spacing: -0.04em;
        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        opacity: 0.72;
        max-width: 720px;
        line-height: 1.6;
        margin-bottom: 1.2rem;
    }

    /* Status pills */
    .pill-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }

    .pill {
        display: inline-block;
        border: 1px solid rgba(128, 128, 128, 0.35);
        border-radius: 999px;
        padding: 0.32rem 0.7rem;
        font-size: 0.78rem;
        opacity: 0.82;
    }

    /* Workflow */
    .workflow {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.7rem;
        margin-top: 0.7rem;
        margin-bottom: 1.8rem;
    }

    .workflow-step {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 0.85rem 1rem;
    }

    .workflow-number {
        font-size: 0.72rem;
        opacity: 0.55;
        margin-bottom: 0.2rem;
    }

    .workflow-title {
        font-weight: 650;
        font-size: 0.95rem;
    }

    .workflow-description {
        font-size: 0.78rem;
        opacity: 0.62;
        margin-top: 0.2rem;
    }

    /* Section label */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        opacity: 0.55;
        margin-bottom: 0.25rem;
    }

    /* Architecture note */
    .architecture-note {
        border-left: 3px solid rgba(128, 128, 128, 0.45);
        padding-left: 1rem;
        margin-top: 1rem;
        font-size: 0.86rem;
        opacity: 0.72;
        line-height: 1.55;
    }

    /* Footer */
    .footer-note {
        text-align: center;
        font-size: 0.76rem;
        opacity: 0.5;
        margin-top: 3rem;
    }

    /* Mobile */
    @media (max-width: 800px) {
        .workflow {
            grid-template-columns: 1fr 1fr;
        }

        .hero-title {
            font-size: 2.3rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Helper Functions
# =========================================================

def prd_to_markdown(prd):
    """
    Convert the structured PRD into Markdown.
    """

    lines = [
        f"# {prd.title}",
        "",
        "## Executive Summary",
        "",
        prd.executive_summary,
        "",
        "## Problem Statement",
        "",
        prd.problem_statement,
        "",
        "## Target Users",
        "",
    ]

    for item in prd.target_users:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Goals",
            "",
        ]
    )

    for item in prd.goals:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Non-Goals",
            "",
        ]
    )

    for item in prd.non_goals:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## User Stories",
            "",
        ]
    )

    for item in prd.user_stories:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## MVP Scope",
            "",
        ]
    )

    for item in prd.mvp_scope:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Acceptance Criteria",
            "",
        ]
    )

    for item in prd.acceptance_criteria:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Risks",
            "",
        ]
    )

    for item in prd.risks:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Open Questions",
            "",
        ]
    )

    for item in prd.open_questions:
        lines.append(f"- {item}")

    lines.append("")

    return "\n".join(lines)


def clear_previous_results():
    """
    Clear previous AI outputs when a new idea is analyzed.
    """

    for key in [
        "analysis",
        "review",
        "prd",
        "human_instructions",
    ]:
        if key in st.session_state:
            del st.session_state[key]


# =========================================================
# Hero
# =========================================================

st.markdown(
    """
    <div class="hero-label">
        LOCAL-FIRST AI PRODUCT WORKFLOW
    </div>

    <div class="hero-title">
        AI Product Copilot
    </div>

    <div class="hero-subtitle">
        Turn ambiguous product ideas into structured,
        reviewed, and human-approved product requirements.
        Built to explore how AI can assist product decisions
        without replacing product judgment.
    </div>

    <div class="pill-container">
        <span class="pill">Qwen3:8B</span>
        <span class="pill">Ollama</span>
        <span class="pill">LangChain</span>
        <span class="pill">Structured Output</span>
        <span class="pill">Human-in-the-loop</span>
        <span class="pill">Local-first</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Workflow Overview
# =========================================================

# =========================================================
# Workflow Overview
# =========================================================

step_1, step_2, step_3, step_4 = st.columns(4)

with step_1:
    st.caption("01 / DEFINE")
    st.markdown("#### Define")
    st.write(
        "Describe an ambiguous product idea."
    )

with step_2:
    st.caption("02 / ANALYZE")
    st.markdown("#### Analyze")
    st.write(
        "Generate structured requirements."
    )

with step_3:
    st.caption("03 / REVIEW")
    st.markdown("#### Review")
    st.write(
        "Detect assumptions and quality risks."
    )

with step_4:
    st.caption("04 / DECIDE")
    st.markdown("#### Decide")
    st.write(
        "Human input shapes the final PRD."
    )

st.divider()

# =========================================================
# Main Workspace
# =========================================================

input_col, analysis_col = st.columns(
    [0.9, 1.35],
    gap="large",
)


# =========================================================
# Left Column — Define
# =========================================================

with input_col:

    st.markdown(
        '<div class="section-label">01 / DEFINE</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "What are you trying to build?"
    )

    requirement = st.text_area(
        "Product idea",
        placeholder=(
            "Example:\n\n"
            "Build an AI resume screening feature that "
            "helps recruiters quickly identify candidates "
            "who match a job description."
        ),
        height=240,
        label_visibility="collapsed",
    )

    analyze_button = st.button(
        "Analyze Product Idea →",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="architecture-note">
            <b>Local AI</b><br>
            Qwen3:8B runs locally through Ollama.
            Product analysis is returned as validated
            structured output rather than free-form chat.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# Run Analysis
# =========================================================

if analyze_button:

    if not requirement.strip():

        st.warning(
            "Enter a product idea before running the analysis."
        )

    else:

        st.session_state[
            "requirement"
        ] = requirement

        clear_previous_results()

        with st.spinner(
            "Generating structured product analysis..."
        ):

            try:

                analysis = analyze_requirement(
                    requirement
                )

                st.session_state[
                    "analysis"
                ] = analysis

            except Exception as e:

                st.error(
                    f"Product analysis failed: {e}"
                )

        if "analysis" in st.session_state:

            with st.spinner(
                "Running independent quality review..."
            ):

                try:

                    review = review_analysis(
                        requirement,
                        st.session_state[
                            "analysis"
                        ],
                    )

                    st.session_state[
                        "review"
                    ] = review

                except Exception as e:

                    st.error(
                        f"Quality review failed: {e}"
                    )


# =========================================================
# Right Column — Analyze
# =========================================================

with analysis_col:

    st.markdown(
        '<div class="section-label">02 / ANALYZE</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "Structured Product Analysis"
    )

    if "analysis" not in st.session_state:

        st.info(
            "Your structured product analysis will appear "
            "here after you submit a product idea."
        )

    else:

        result = st.session_state[
            "analysis"
        ]

        st.markdown(
            "#### Problem"
        )

        st.write(
            result.problem
        )

        st.markdown(
            "#### Target Users"
        )

        for user in result.target_users:

            st.markdown(
                f"- {user}"
            )

        st.markdown(
            "#### User Stories"
        )

        for story in result.user_stories:

            st.markdown(
                f"- **As a {story.role}**, "
                f"I want to {story.goal}, "
                f"so that {story.benefit}."
            )

        st.markdown(
            "#### MVP Features"
        )

        for feature in result.mvp_features:

            st.markdown(
                f"- {feature}"
            )

        st.markdown(
            "#### Acceptance Criteria"
        )

        for criterion in (
            result.acceptance_criteria
        ):

            st.markdown(
                f"- {criterion}"
            )

        with st.expander(
            "Risks, assumptions & open questions",
            expanded=False,
        ):

            st.markdown(
                "##### Risks"
            )

            for risk in result.risks:

                st.markdown(
                    f"- {risk}"
                )

            st.markdown(
                "##### Assumptions"
            )

            for assumption in result.assumptions:

                st.markdown(
                    f"- {assumption}"
                )

            st.markdown(
                "##### Open Questions"
            )

            for question in result.open_questions:

                st.markdown(
                    f"- {question}"
                )


# =========================================================
# Quality Review
# =========================================================

if "review" in st.session_state:

    st.divider()

    st.markdown(
        '<div class="section-label">03 / REVIEW</div>',
        unsafe_allow_html=True,
    )

    review_title_col, review_status_col = st.columns(
        [3, 1]
    )

    with review_title_col:

        st.subheader(
            "AI Quality Review"
        )

        st.caption(
            "A second model pass critiques the generated "
            "analysis. Findings are advisory, not ground truth."
        )

    review = st.session_state[
        "review"
    ]

    with review_status_col:

        if review.passed:

            st.success(
                "Review passed"
            )

        else:

            st.warning(
                f"{len(review.issues)} issues detected"
            )

    if not review.passed:

        for index, issue in enumerate(
            review.issues,
            start=1,
        ):

            with st.expander(
                f"{index}. {issue.category}",
                expanded=False,
            ):

                st.markdown(
                    "**Issue**"
                )

                st.write(
                    issue.issue
                )

                st.markdown(
                    "**Recommendation**"
                )

                st.write(
                    issue.recommendation
                )


# =========================================================
# Human Review
# =========================================================

if (
    "analysis" in st.session_state
    and "review" in st.session_state
):

    st.divider()

    st.markdown(
        '<div class="section-label">04 / DECIDE</div>',
        unsafe_allow_html=True,
    )

    decision_col, context_col = st.columns(
        [1.4, 0.8],
        gap="large",
    )

    with decision_col:

        st.subheader(
            "Human Product Decision"
        )

        st.write(
            "Review the AI output, then add the product "
            "decisions that should shape the final PRD."
        )

        human_instructions = st.text_area(
            "Product Manager Instructions",
            placeholder=(
                "Example:\n\n"
                "Remove automated candidate ranking from MVP.\n\n"
                "Recruiters must make the final shortlist "
                "decision.\n\n"
                "Show evidence for each AI recommendation.\n\n"
                "Treat candidate privacy as a key risk."
            ),
            height=220,
            key="human_instructions",
        )

        generate_prd_button = st.button(
            "Generate Human-Reviewed PRD →",
            type="primary",
            use_container_width=True,
        )

    with context_col:

        st.markdown(
            """
            <div class="architecture-note">
                <b>Why human review?</b><br><br>

                The quality reviewer is another LLM,
                not an authority.

                Human instructions therefore take priority
                when the final PRD is generated.
                This keeps consequential product decisions
                under human control.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =====================================================
    # Generate Final PRD
    # =====================================================

    if generate_prd_button:

        with st.spinner(
            "Generating human-reviewed PRD..."
        ):

            try:

                prd = generate_prd(
                    st.session_state[
                        "requirement"
                    ],
                    st.session_state[
                        "analysis"
                    ],
                    st.session_state[
                        "review"
                    ],
                    human_instructions,
                )

                st.session_state[
                    "prd"
                ] = prd

            except Exception as e:

                st.error(
                    "PRD generation failed: "
                    f"{e}"
                )


# =========================================================
# Final PRD
# =========================================================

if "prd" in st.session_state:

    prd = st.session_state[
        "prd"
    ]

    st.divider()

    st.markdown(
        '<div class="section-label">OUTPUT</div>',
        unsafe_allow_html=True,
    )

    st.subheader(
        "Final Product Requirements Document"
    )

    st.caption(
        "Generated from the original idea, structured "
        "analysis, AI critique, and human product decisions."
    )

    st.markdown(
        f"# {prd.title}"
    )

    st.markdown(
        "### Executive Summary"
    )

    st.write(
        prd.executive_summary
    )

    st.markdown(
        "### Problem Statement"
    )

    st.write(
        prd.problem_statement
    )

    prd_left, prd_right = st.columns(
        2,
        gap="large",
    )

    with prd_left:

        st.markdown(
            "### Target Users"
        )

        for item in prd.target_users:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### Goals"
        )

        for item in prd.goals:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### User Stories"
        )

        for item in prd.user_stories:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### MVP Scope"
        )

        for item in prd.mvp_scope:

            st.markdown(
                f"- {item}"
            )

    with prd_right:

        st.markdown(
            "### Non-Goals"
        )

        for item in prd.non_goals:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### Acceptance Criteria"
        )

        for item in prd.acceptance_criteria:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### Risks"
        )

        for item in prd.risks:

            st.markdown(
                f"- {item}"
            )

        st.markdown(
            "### Open Questions"
        )

        for item in prd.open_questions:

            st.markdown(
                f"- {item}"
            )


    # =====================================================
    # Download
    # =====================================================

    st.divider()

    download_col, note_col = st.columns(
        [1, 2],
        gap="large",
    )

    markdown_prd = prd_to_markdown(
        prd
    )

    with download_col:

        st.download_button(
            label="Download PRD (.md)",
            data=markdown_prd,
            file_name=(
                "product_requirements_document.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )

    with note_col:

        st.caption(
            "The exported document remains a draft. "
            "AI-generated requirements should be validated "
            "with users, product stakeholders, and "
            "engineering before implementation."
        )


# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div class="footer-note">
        AI Product Copilot · Qwen3:8B · Ollama · LangChain ·
        Local-first · Human-in-the-loop
    </div>
    """,
    unsafe_allow_html=True,
)