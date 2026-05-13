# OranGPT

Placeholder README for the OranGPT Streamlit dashboard project.

## Project Structure

```text
orangpt/
├── app.py                    # Streamlit UI layer
├── ai/
│   ├── __init__.py
│   └── classifier.py         # Formal/informal classification logic
├── utils/
│   ├── __init__.py
│   └── text_utils.py         # Shared helper utilities
├── assets/
│   └── logo.svg              # Static assets (logo, images)
├── tests/
│   └── test_classifier.py    # Focused unit tests
├── .env                      # Local configuration values
└── requirements.txt
```

## Team Focus (3 Developers)

- **Developer 1 (UI/UX):** `app.py` and `assets/` for Streamlit layout, controls, and visual updates.
- **Developer 2 (AI Logic):** `ai/classifier.py` for classification behavior and model/rules updates.
- **Developer 3 (Platform/Quality):** `utils/`, `tests/`, `.env`, and dependency/config hygiene (`requirements.txt`).

This split keeps ownership clear and reduces merge conflicts across independent areas.

## How to run
```bash
streamlit run app.py
```
