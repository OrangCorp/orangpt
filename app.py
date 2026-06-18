import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from ai.classifier import TextClassifier
from ai.slmclass import FormalityScorer
from utils.text_utils import highlight_words

load_dotenv()

APP_TITLE = os.getenv("ORANGPT_APP_TITLE", "OranGPT Formality Checker")
COMMUNITY_NAME = os.getenv("ORANGPT_COMMUNITY", "Orang")


def init_session_state() -> None:
    """Initialize session state variables to ensure results persist."""
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
        st.session_state.results = {}


def render_header() -> None:
    """Render the application header with logo and title."""
    logo_path = Path("assets/logo.png")

    # Modern Streamlit column alignment ensures the logo and text are vertically centered
    col_logo, col_title = st.columns([1, 8], vertical_alignment="center")

    with col_logo:
        if logo_path.exists():
            st.image(str(logo_path), width=80)

    with col_title:
        st.title(APP_TITLE)
        st.caption(f"Check whether text is formal or informal for the {COMMUNITY_NAME} community.")


def render_sidebar() -> tuple[str, str]:
    """Render sidebar configuration widgets and return selected options."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.caption("Adjust model settings and preferences here.")

        selected_language = st.selectbox(
            "Select Language",
            options=["English", "Polish"],
            index=0,
            help="Choose the primary language for tone analysis."
        )

        selected_model = st.selectbox(
            "Select AI Model",
            options=["Standard Classifier", "Small Language Model (SLM)"],
            index=0,
            help="Choose the backend model used for tone evaluation."
        )

        return selected_language, selected_model


def classify_tone(text: str, language: str, model: str):
    """Route tone classification to the selected backend model."""
    if model == "Small Language Model (SLM)":
        classifier = FormalityScorer()
    else:
        classifier = TextClassifier()

    tone, confidence, formal_prob = classifier.classify_tone(text, language, model)
    return tone, confidence, formal_prob, classifier


def run_analysis(text: str, language: str, model: str) -> None:
    """Execute the classification and store results securely in session state."""
    if not text.strip():
        st.warning("Please enter some text to classify.", icon="⚠️")
        return

    # Use st.status for a more robust user-feedback micro-interaction
    with st.status("Analyzing tone...", expanded=True) as status:
        st.write(f"Routing text to {model}...")
        tone, confidence, formal_prob, classifier = classify_tone(text, language, model)

        st.write("Generating visual text highlights...")
        highlighted_html = highlight_words(text, language, model, classifier)

        status.update(label="Analysis complete!", state="complete", expanded=False)

    # Persist data so sidebar interactions don't reset the view
    st.session_state.analysis_complete = True
    st.session_state.results = {
        "tone": tone,
        "confidence": confidence,
        "formal_prob": formal_prob,
        "highlighted_html": highlighted_html,
        "language": language,
        "model": model
    }


def render_results() -> None:
    """Render the analysis results directly from the session state."""
    res = st.session_state.results
    formal_prob = res["formal_prob"]
    confidence = res["confidence"]
    slider_pos = int(formal_prob * 100)

    st.markdown("### Analysis Results")

    # Use native Streamlit containers to build modern visual cards
    with st.container(border=True):
        res_col1, res_col2 = st.columns([1, 2], gap="large")

        with res_col1:
            st.subheader("Overall Tone")

            if formal_prob >= 0.85:
                status_text = "👔 Highly Formal"
            elif formal_prob >= 0.60:
                status_text = "💼 Somewhat Formal"
            elif formal_prob >= 0.40:
                status_text = "⚖️ Neutral / Balanced"
            elif formal_prob >= 0.15:
                status_text = "🛹 Somewhat Informal"
            else:
                status_text = "🔥 Highly Informal"

            st.markdown(f"#### {status_text}")

            # Theme-agnostic HTML/CSS: Removed hardcoded colors, using standard opacities
            st.markdown(
                f"""
                <div style="margin-top: 20px; margin-bottom: 5px; font-size: 0.85em; display: flex; justify-content: space-between; opacity: 0.7;">
                    <span>🛹 Informal</span>
                    <span>Neutral</span>
                    <span>Formal 👔</span>
                </div>
                <div style="position: relative; width: 100%; height: 16px; background: linear-gradient(to right, #ef233c 0%, #4a4e69 50%, #00b4d8 100%); border-radius: 8px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.3); margin-bottom: 10px;">
                    <div style="position: absolute; left: calc({slider_pos}% - 6px); top: -4px; width: 12px; height: 24px; background-color: #ffffff; border-radius: 4px; box-shadow: 0px 2px 5px rgba(0,0,0,0.4);"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")  # Spacer

            # Replaced raw HTML text with clean, modern Streamlit metric modules
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric(label="Formality Index", value=f"{slider_pos}%")
            with metric_col2:
                st.metric(label="Confidence", value=f"{confidence:.1%}")

        with res_col2:
            st.subheader("Highlighted Text")
            st.markdown(
                f"""
                <div style="font-size: 1.1em; line-height: 1.7; white-space: normal; word-break: break-word;">
                    {res["highlighted_html"]}
                </div>
                """,
                unsafe_allow_html=True
            )


def main() -> None:
    """Run the main Streamlit application."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🟠", layout="wide")

    # Inject global CSS
    st.markdown(
        """
        <style>
            div[data-baseweb="select"] span {
                white-space: normal !important;
                word-wrap: break-word !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    init_session_state()
    selected_language, selected_model = render_sidebar()
    render_header()

    with st.container():
        text = st.text_area(
            "Enter text for analysis:",
            placeholder="Type a sentence to classify...",
            height=150
        )

        if st.button("Classify Tone", type="primary"):
            run_analysis(text, selected_language, selected_model)

    if st.session_state.analysis_complete:
        st.divider()
        render_results()


if __name__ == "__main__":
    main()
