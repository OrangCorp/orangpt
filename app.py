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

def main() -> None:
    """Run the main Streamlit application."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🟠", layout="wide")

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

    logo_path = Path("assets/logo.svg")
    col_logo, col_title = st.columns([1, 8])
    
    with col_logo:
        if logo_path.exists():
            st.image(str(logo_path), width=80)
            
    with col_title:
        st.title(APP_TITLE)
        st.caption(f"Check whether text is formal or informal for the {COMMUNITY_NAME} community.")

    st.divider()

    text = st.text_area(
        "Enter text for analysis:", 
        placeholder="Type a sentence to classify...",
        height=150
    )
    classifier =  TextClassifier() 
    if st.button("Classify Tone", type="primary", use_container_width=False):
        if not text.strip():
            st.warning("Please enter some text to classify.")
        else:
            with st.spinner(f"Analyzing tone using {selected_model}..."):
                tone, confidence, formal_prob = classifier.classify_tone(text, selected_language, selected_model)   
                highlighted_html = highlight_words(text, selected_language, selected_model,classifier)

            st.markdown("### Analysis Results")
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
                
                slider_pos = int(formal_prob * 100)
                
                st.markdown(
                    f"""
                    <div style="margin-top: 15px; margin-bottom: 5px; font-size: 0.85em; display: flex; justify-content: space-between; color: #aaa;">
                        <span>🛹 Informal</span>
                        <span>Neutral</span>
                        <span>Formal 👔</span>
                    </div>
                    <div style="position: relative; width: 100%; height: 16px; background: linear-gradient(to right, #ef233c 0%, #4a4e69 50%, #00b4d8 100%); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);">
                        <div style="position: absolute; left: calc({slider_pos}% - 6px); top: -4px; width: 12px; height: 22px; background-color: #fff; border-radius: 3px; box-shadow: 0px 1px 5px rgba(0,0,0,0.5);"></div>
                    </div>
                    <div style="text-align: center; font-size: 0.9em; margin-top: 12px; color: #bbb;">
                        Formality Index: <b>{slider_pos}%</b> | Confidence: <b>{confidence:.1%}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(f"**Language:** {selected_language}")
                st.caption(f"**Model:** {selected_model}")

            with res_col2:
                st.subheader("Highlighted Analysis")
                st.markdown(
                    """
                    <div style="margin-bottom: 15px; font-size: 0.9em; color: #bbb;">
                        <b>Legend (Opacity intensity shows weight):</b> 
                        <span style="background-color: rgba(0, 180, 216, 0.8); color: #fff; padding: 2px 6px; border-radius: 4px; font-weight: bold;">Formal</span>
                        <span style="background-color: rgba(239, 35, 60, 0.8); color: #fff; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-left: 10px;">Informal</span>
                        <span style="margin-left: 10px; color: #888;">Plain Text = Neutral</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Removed fixed light (#fafafa) backgrounds for dark theme styling consistency
                st.markdown(
                    f"""
                    <div style="border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 8px; font-size: 1.1em; line-height: 1.7; background-color: rgba(255, 255, 255, 0.04); color: inherit; white-space: normal; word-break: break-word;">
                        {highlighted_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()