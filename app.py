import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from ai.classifier import classify_tone
from utils.text_utils import highlight_words

load_dotenv()

# --- Configuration & Environment Variables ---
APP_TITLE = os.getenv("ORANGPT_APP_TITLE", "OranGPT Formality Checker")
COMMUNITY_NAME = os.getenv("ORANGPT_COMMUNITY", "Orang")

def main() -> None:
    """Run the main Streamlit application."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🟠", layout="wide")

    # --- Custom CSS for UI Tweaks ---
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

    # --- Sidebar Configuration ---
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

        st.divider()
        st.markdown(f"**Target Community:**\n{COMMUNITY_NAME}")

    # --- Main Content Area ---
    logo_path = Path("assets/logo.svg")
    col_logo, col_title = st.columns([1, 8])
    
    with col_logo:
        if logo_path.exists():
            st.image(str(logo_path), width=80)
            
    with col_title:
        st.title(APP_TITLE)
        st.caption(f"Check whether text is formal or informal for the {COMMUNITY_NAME} community.")

    st.divider()

    # --- Input Section ---
    text = st.text_area(
        "Enter text for analysis:", 
        placeholder="Type a sentence to classify (e.g., 'hey bro this is gonna be awesome!')...",
        height=150
    )

    if st.button("Classify Tone", type="primary", use_container_width=False):
        if not text.strip():
            st.warning("Please enter some text to classify.")
        else:
            with st.spinner(f"Analyzing tone using {selected_model}..."):
                # Pass only text to match classifier.py's current strict signature
                tone = classify_tone(text)
                
                # HTML formatter still takes language/model to swap out vocabularies 
                highlighted_html = highlight_words(text, selected_language, selected_model)

            # --- Results Layout using Columns ---
            st.markdown("### Analysis Results")
            res_col1, res_col2 = st.columns([1, 2], gap="large")

            with res_col1:
                st.subheader("Overall Tone")
                tone_normalized = str(tone).lower().strip()
                
                if tone_normalized == "formal":
                    st.success("👔 **Formal**")
                elif tone_normalized == "informal":
                    st.error("🛹 **Informal**")
                else: 
                    st.info(f"⚖️ **Unknown / Neutral**")

                st.caption(f"**Language:** {selected_language}")
                st.caption(f"**Model:** {selected_model}")

            with res_col2:
                st.subheader("Highlighted Analysis")
                st.markdown(
                    """
                    <div style="margin-bottom: 15px; font-size: 0.9em;">
                        <b>Legend:</b> 
                        <span style="background-color: #d1ecf1; color: #0c5460; padding: 2px 6px; border-radius: 4px;">Formal</span>
                        <span style="background-color: #f8d7da; color: #721c24; padding: 2px 6px; border-radius: 4px; margin-left: 10px;">Informal</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 8px; font-size: 1.1em; line-height: 1.6;">
                        {highlighted_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()