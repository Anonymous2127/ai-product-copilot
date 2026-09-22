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
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .hero-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        opacity: 0.55;
        margin-bottom: 0.6rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 760;
        line-height: 1.05;
        letter-spacing: -0.04em;
        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.65;
        opacity: 0.7;
        max-width: 760px;
        margin-bottom: 1rem;
    }

    .pill {
        display: inline-block;
        border: 1px solid rgba(128,128,128,0.3);
        border-radius: 999px;
        padding: 0.3rem 0.65rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        font-size: 0.76rem;
        opacity: 0.8;
    }

    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        opacity: 0.5;
        margin-bottom: 0.25rem;
    }

    .small-note {
        border-left: 3px solid rgba(128,128,128,0.35);
        padding-left: 1rem;
        font-size: 0.86rem;
        opacity: 0.72;
        line-height: 1.6;
        margin-top: 1rem;
    }

    .decision-summary {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.8rem;
    }

    .footer {
        text-align: center;
        opacity: 0.45;
        font-size: 0.76rem;
        margin-top: 4rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Helpers
# =========================================================

def clear_workflow():
    keys = [
        "analysis",
        "review",
        "prd",
        "requirement",
        "human_instructions",
        "remove_ranking",
        "require_evidence",
        "human_shortlist",
        "privacy_risk",
        "no_ats",
    ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def prd_to_markdown(prd):

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

    sections = [
        ("Goals", prd.goals),
        ("Non-Goals", prd.non_goals),
        ("User Stories", prd.user_stories),
        ("MVP Scope", prd.mvp_scope),
        (
            "Acceptance Criteria",
            prd.acceptance_criteria,
        ),
        ("Risks", prd.risks),
        ("Open Questions", prd.open_questions),
    ]

    for title, items in sections:

        lines.extend(
            [
                "",
                f"## {title}",
                "",
            ]
        )

        for item in items:
            lines.append(f"- {item}")

    lines.append("")

    return "\n".join(lines)


def build_human_instructions(
    remove_ranking,
    require_evidence,
    human_shortlist,
    privacy_risk,
    no_ats,
    additional_notes,
):

    instructions = []

    if remove_ranking:
        instructions.append(
            "Remove automated candidate ranking and "
            "relevance scores from the MVP."
        )

    if require_evidence:
        instructions.append(
            "Every AI-generated match should show "
            "supporting evidence from the resume."
        )

    if human_shortlist:
        instructions.append(
            "Recruiters must make the final shortlist "
            "decision. AI should only assist."
        )

    if privacy_risk:
        instructions.append(
            "Candidate privacy and sensitive personal data "
            "must be treated as a key product risk."
        )

    if no_ats:
        instructions.append(
            "Do not assume ATS integration in the MVP."
        )

    if additional_notes.strip():
        instructions.append(
            additional_notes.strip()
        )

    if not instructions:
        return (
            "No additional human product decisions "
            "were provided."
        )

    return "\n\n".join(instructions)


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
        Turn ambiguous ideas into structured product decisions.
        AI proposes and critiques. Product managers decide.
    </div>

    <span class="pill">Qwen3:8B</span>
    <span class="pill">Ollama</span>
    <span class="pill">LangChain</span>
    <span class="pill">Pydantic</span>
    <span class="pill">Human-in-the-loop</span>
    """,
    unsafe_allow_html=True,
)

st.write("")


# =========================================================
# Progress Navigation
# =========================================================

nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if "analysis" in st.session_state:
        st.success("✓ 01 Define")
    else:
        st.info("● 01 Define")

with nav2:
    if "analysis" in st.session_state:
        st.success("✓ 02 Analyze")
    else:
        st.caption("○ 02 Analyze")

with nav3:
    if "review" in st.session_state:
        st.success("✓ 03 Review")
    else:
        st.caption("○ 03 Review")

with nav4:
    if "prd" in st.session_state:
        st.success("✓ 04 Decide")
    elif "review" in st.session_state:
        st.info("● 04 Decide")
    else:
        st.caption("○ 04 Decide")

with nav5:
    if "prd" in st.session_state:
        st.success("✓ 05 PRD")
    else:
        st.caption("○ 05 PRD")

st.divider()


# =========================================================
# STEP 1 — DEFINE
# =========================================================

if "analysis" not in st.session_state:

    st.markdown(
        '<div class="section-label">01 / DEFINE</div>',
        unsafe_allow_html=True,
    )

    st.header(
        "What are you trying to build?"
    )

    st.write(
        "Start with an early product idea. "
        "It does not need to be a complete requirement."
    )

    input_col, example_col = st.columns(
        [1.5, 0.8],
        gap="large",
    )

    with input_col:

        requirement = st.text_area(
            "Product idea",
            placeholder=(
                "Build an AI resume screening feature "
                "that helps recruiters identify candidates "
                "who match a job description."
            ),
            height=190,
            label_visibility="collapsed",
        )

        analyze_button = st.button(
            "Analyze Product Idea →",
            type="primary",
            use_container_width=True,
        )

    with example_col:

        st.markdown(
            "#### Example"
        )

        st.caption(
            "Try this product idea:"
        )

        st.code(
            "Build an AI resume screening feature "
            "that helps recruiters identify candidates "
            "who match a job description.",
            language=None,
        )

        st.markdown(
            """
            <div class="small-note">
                <b>Local inference</b><br>
                Product inputs are processed by
                Qwen3:8B through Ollama.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if analyze_button:

        if not requirement.strip():

            st.warning(
                "Enter a product idea first."
            )

        else:

            clear_workflow()

            st.session_state[
                "requirement"
            ] = requirement

            with st.spinner(
                "Analyzing product idea..."
            ):

                try:

                    analysis = analyze_requirement(
                        requirement
                    )

                    st.session_state[
                        "analysis"
                    ] = analysis

                    review = review_analysis(
                        requirement,
                        analysis,
                    )

                    st.session_state[
                        "review"
                    ] = review

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Analysis failed: {e}"
                    )


# =========================================================
# STEP 2 + 3 — ANALYZE / REVIEW
# =========================================================

elif (
    "analysis" in st.session_state
    and "prd" not in st.session_state
):

    analysis = st.session_state[
        "analysis"
    ]

    review = st.session_state.get(
        "review"
    )

    analysis_col, review_col = st.columns(
        [1.15, 0.85],
        gap="large",
    )

    # -----------------------------------------------------
    # Analysis
    # -----------------------------------------------------

    with analysis_col:

        st.markdown(
            '<div class="section-label">'
            '02 / ANALYZE'
            '</div>',
            unsafe_allow_html=True,
        )

        st.header(
            "AI Product Analysis"
        )

        st.markdown(
            "### Problem"
        )

        st.write(
            analysis.problem
        )

        st.markdown(
            "### Target Users"
        )

        for item in analysis.target_users:
            st.markdown(f"- {item}")

        st.markdown(
            "### MVP Features"
        )

        for item in analysis.mvp_features:
            st.markdown(f"- {item}")

        with st.expander(
            "View user stories"
        ):

            for story in analysis.user_stories:

                st.markdown(
                    f"- **As a {story.role}**, "
                    f"I want to {story.goal}, "
                    f"so that {story.benefit}."
                )

        with st.expander(
            "View acceptance criteria"
        ):

            for item in (
                analysis.acceptance_criteria
            ):
                st.markdown(f"- {item}")

        with st.expander(
            "View risks & assumptions"
        ):

            st.markdown(
                "#### Risks"
            )

            for item in analysis.risks:
                st.markdown(f"- {item}")

            st.markdown(
                "#### Assumptions"
            )

            for item in analysis.assumptions:
                st.markdown(f"- {item}")

            st.markdown(
                "#### Open Questions"
            )

            for item in analysis.open_questions:
                st.markdown(f"- {item}")

    # -----------------------------------------------------
    # Quality Review
    # -----------------------------------------------------

    with review_col:

        st.markdown(
            '<div class="section-label">'
            '03 / REVIEW'
            '</div>',
            unsafe_allow_html=True,
        )

        st.header(
            "AI Quality Review"
        )

        st.caption(
            "A second model pass challenges the "
            "first AI response."
        )

        if review is None:

            st.warning(
                "Quality review unavailable."
            )

        elif review.passed:

            st.success(
                "No major issues detected."
            )

        else:

            st.warning(
                f"{len(review.issues)} "
                "decisions worth reviewing"
            )

            for index, issue in enumerate(
                review.issues,
                start=1,
            ):

                with st.expander(
                    f"{index}. {issue.category}",
                    expanded=(index == 1),
                ):

                    st.markdown(
                        "**Why this matters**"
                    )

                    st.write(
                        issue.issue
                    )

                    st.markdown(
                        "**AI recommendation**"
                    )

                    st.write(
                        issue.recommendation
                    )

        st.markdown(
            """
            <div class="small-note">
                <b>The reviewer is not ground truth.</b><br>
                Its findings are advisory.
                The product manager makes the
                final product decision.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =====================================================
    # Decision Workspace
    # =====================================================

    st.divider()

    st.markdown(
        '<div class="section-label">'
        '04 / DECIDE'
        '</div>',
        unsafe_allow_html=True,
    )

    st.header(
        "Product Decision Workspace"
    )

    st.write(
        "Turn AI suggestions into explicit product decisions "
        "before generating the PRD."
    )

    decision_col, explanation_col = st.columns(
        [1.25, 0.75],
        gap="large",
    )

    with decision_col:

        remove_ranking = st.checkbox(
            "Remove automated candidate ranking "
            "and relevance scores",
            value=True,
            key="remove_ranking",
        )

        require_evidence = st.checkbox(
            "Require supporting evidence for "
            "AI-generated matches",
            value=True,
            key="require_evidence",
        )

        human_shortlist = st.checkbox(
            "Keep final shortlist decisions "
            "with recruiters",
            value=True,
            key="human_shortlist",
        )

        privacy_risk = st.checkbox(
            "Treat candidate privacy as a "
            "key product risk",
            value=True,
            key="privacy_risk",
        )

        no_ats = st.checkbox(
            "Keep ATS integration outside "
            "the MVP",
            value=True,
            key="no_ats",
        )

        additional_notes = st.text_area(
            "Additional PM notes",
            placeholder=(
                "Add any product decision that "
                "is not covered above..."
            ),
            height=120,
            key="human_instructions",
        )

    with explanation_col:

        st.markdown(
            "#### Why this step exists"
        )

        st.write(
            "AI analysis can surface useful options, "
            "but product scope and consequential "
            "decisions should not be silently determined "
            "by model output."
        )

        st.info(
            "Human decisions take priority over "
            "AI reviewer recommendations."
        )

    st.write("")

    generate_button = st.button(
        "Generate Human-Reviewed PRD →",
        type="primary",
        use_container_width=True,
    )

    if generate_button:

        human_instructions = (
            build_human_instructions(
                remove_ranking,
                require_evidence,
                human_shortlist,
                privacy_risk,
                no_ats,
                additional_notes,
            )
        )

        with st.spinner(
            "Applying product decisions..."
        ):

            try:

                prd = generate_prd(
                    st.session_state[
                        "requirement"
                    ],
                    analysis,
                    review,
                    human_instructions,
                )

                st.session_state[
                    "prd"
                ] = prd

                st.session_state[
                    "final_human_instructions"
                ] = human_instructions

                st.rerun()

            except Exception as e:

                st.error(
                    f"PRD generation failed: {e}"
                )


# =========================================================
# STEP 5 — FINAL PRD
# =========================================================

elif "prd" in st.session_state:

    prd = st.session_state[
        "prd"
    ]

    st.markdown(
        '<div class="section-label">'
        '05 / PRD'
        '</div>',
        unsafe_allow_html=True,
    )

    st.success(
        "Human-reviewed PRD generated"
    )

    st.header(
        prd.title
    )

    st.write(
        prd.executive_summary
    )


    # =====================================================
    # Before / After
    # =====================================================

    st.subheader(
        "What changed after human review?"
    )

    st.caption(
        "The final PRD reflects explicit product "
        "decisions rather than automatically accepting "
        "the initial AI proposal."
    )

    before_col, after_col = st.columns(
        2,
        gap="large",
    )

    with before_col:

        st.markdown(
            "#### AI Proposal"
        )

        st.markdown(
            """
            - Automated candidate ranking
            - Relevance scoring
            - AI-assisted shortlisting
            - Matching without required evidence
            - ATS integration left ambiguous
            """
        )

    with after_col:

        st.markdown(
            "#### Human Decision"
        )

        if st.session_state.get(
            "remove_ranking",
            False,
        ):
            st.markdown(
                "✓ Ranking removed from MVP"
            )

        if st.session_state.get(
            "require_evidence",
            False,
        ):
            st.markdown(
                "✓ Supporting evidence required"
            )

        if st.session_state.get(
            "human_shortlist",
            False,
        ):
            st.markdown(
                "✓ Recruiter keeps final decision"
            )

        if st.session_state.get(
            "privacy_risk",
            False,
        ):
            st.markdown(
                "✓ Candidate privacy made explicit"
            )

        if st.session_state.get(
            "no_ats",
            False,
        ):
            st.markdown(
                "✓ ATS integration moved outside MVP"
            )


    # =====================================================
    # PRD Content
    # =====================================================

    st.divider()

    st.subheader(
        "Final Product Requirements Document"
    )

    st.markdown(
        "### Problem Statement"
    )

    st.write(
        prd.problem_statement
    )

    left, right = st.columns(
        2,
        gap="large",
    )

    with left:

        st.markdown(
            "### Target Users"
        )

        for item in prd.target_users:
            st.markdown(f"- {item}")

        st.markdown(
            "### Goals"
        )

        for item in prd.goals:
            st.markdown(f"- {item}")

        st.markdown(
            "### User Stories"
        )

        for item in prd.user_stories:
            st.markdown(f"- {item}")

        st.markdown(
            "### MVP Scope"
        )

        for item in prd.mvp_scope:
            st.markdown(f"- {item}")

    with right:

        st.markdown(
            "### Non-Goals"
        )

        for item in prd.non_goals:
            st.markdown(f"- {item}")

        st.markdown(
            "### Acceptance Criteria"
        )

        for item in (
            prd.acceptance_criteria
        ):
            st.markdown(f"- {item}")

        st.markdown(
            "### Risks"
        )

        for item in prd.risks:
            st.markdown(f"- {item}")

        st.markdown(
            "### Open Questions"
        )

        for item in prd.open_questions:
            st.markdown(f"- {item}")


    # =====================================================
    # Export / Restart
    # =====================================================

    st.divider()

    download_col, restart_col = st.columns(
        2
    )

    markdown_prd = prd_to_markdown(
        prd
    )

    with download_col:

        st.download_button(
            "Download PRD (.md)",
            data=markdown_prd,
            file_name=(
                "product_requirements_document.md"
            ),
            mime="text/markdown",
            use_container_width=True,
        )

    with restart_col:

        if st.button(
            "Start New Product Idea",
            use_container_width=True,
        ):

            clear_workflow()

            if (
                "final_human_instructions"
                in st.session_state
            ):
                del st.session_state[
                    "final_human_instructions"
                ]

            st.rerun()


# =========================================================
# Footer
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI Product Copilot · Qwen3:8B · Ollama ·
        LangChain · Pydantic · Human-in-the-loop
    </div>
    """,
    unsafe_allow_html=True,
)