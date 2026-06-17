# OranGPT

OranGPT is a Streamlit app for classifying text as formal or informal in English and Polish. It combines a lightweight web UI, pre-trained scikit-learn models, and LIME-based highlighting so users can see both the predicted tone and the words that influenced it most.

Live demo: https://orangcorp-orangpt-app-no-gpu-branch-5vccpl.streamlit.app/

## Features

- Bilingual tone analysis for English and Polish.
- Choice of model from the sidebar, with pre-trained models shipped in the repository.
- Tone summary with confidence and a formality index.
- Word-level highlighting to show which parts of the text pushed the decision toward formal or informal language.
- Session-state driven Streamlit UI so results stay visible while the sidebar changes.

## Tech Stack

- Python
- Streamlit
- pandas
- scikit-learn
- LIME
- joblib

## Repository Layout

```text
orangpt/
├── app.py                  # Streamlit entry point and UI
├── ai/
│   ├── __init__.py
│   ├── classifier.py       # Model loading, training, and prediction logic
│   └── models/             # Pre-trained model artifacts and metadata
├── assets/
│   └── logo.png            # Application branding asset
├── extracted_data/         # Training data and data prep helpers
├── tests/
│   └── test_classifier.py  # Unit tests for classifier behavior
├── utils/
│   ├── __init__.py
│   └── text_utils.py       # Text normalization and highlighting helpers
├── docs/
│   └── raport.md           # Project report and methodology notes
├── requirements.txt        # Python dependencies
└── README.md
```

## How It Works

The app takes user input, routes it through the selected language and model, then returns:

1. A formal/informal label.
2. A confidence score.
3. A formality probability used to render the visual gauge.
4. Highlighted text that marks influential formal and informal tokens.

The current repository ships a standard classifier pipeline backed by TF-IDF features and an ensemble of classical machine-learning models. Model artifacts for English and Polish are stored in `ai/models/`.

## Prerequisites

- Python 3.10 or newer.
- A virtual environment is recommended.

## Local Setup

```bash
git clone <repository-url>
cd orangpt
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

The app reads optional environment variables from a local `.env` file:

- `ORANGPT_APP_TITLE` - custom title shown in the Streamlit header.
- `ORANGPT_COMMUNITY` - community name used in the subtitle.

Example:

```env
ORANGPT_APP_TITLE=OranGPT Formality Checker
ORANGPT_COMMUNITY=Orang
```

## Run the App

```bash
streamlit run app.py
```

Then open the local Streamlit URL printed in the terminal.

## Testing

```bash
python -m unittest discover tests
```

## Data and Models

- Training data lives in `extracted_data/` as compressed CSV files for English and Polish formality classes.
- Pre-trained model files are stored in `ai/models/`.
- If a requested standard model file is missing, the classifier code can retrain and save it again.

## Deployment

The project is deployed on Streamlit at:

https://orangcorp-orangpt-app-no-gpu-branch-5vccpl.streamlit.app/

## Project Notes

- The UI is built around Streamlit session state, so analysis results persist while users adjust sidebar settings.
- The visualization uses color-coded highlights to distinguish formal and informal signals.
- The project report in `docs/raport.md` contains the broader methodology and background for the formality-classification work.
