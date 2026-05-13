"""Streamlit UI for OranGPT."""

import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st

from ai.classifier import classify_tone

load_dotenv()

APP_TITLE = os.getenv("ORANGPT_APP_TITLE", "OranGPT Formality Checker")
COMMUNITY_NAME = os.getenv("ORANGPT_COMMUNITY", "Orang")


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🟠")
    st.title(APP_TITLE)
    st.caption(f"Check whether text is formal or informal for the {COMMUNITY_NAME} community.")

    logo_path = Path("assets/logo.svg")
    if logo_path.exists():
        st.image(str(logo_path), width=120)

    text = st.text_area("Enter text", placeholder="Type a sentence to classify...")
    if st.button("Classify"):
        tone = classify_tone(text)
        st.success(f"Result: **{tone}**")


if __name__ == "__main__":
    main()
