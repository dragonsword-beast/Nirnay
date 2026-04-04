# Nirnay 

Nirnay is a Streamlit-based clinical workflow dashboard for AI-assisted medical intake, image support, and chat assistant interactions.

## What this app does

- Provides a patient intake profile page with name, age, gender, disclaimer consent, and saved workflow support.
- Offers a clinical analysis flow with structured UI, image upload support, and AI-guided report generation.
- Includes a chat assistant page with medical and quick-response chat modes backed by the `groq` SDK.
- Uses a polished custom UI with responsive styling and a dark, clinical dashboard aesthetic.

## Files

- `Nirnay.py` - Main Streamlit application file.
- `requirements.txt` - Python dependencies for the app.
- `README.md` - Project documentation.

## Requirements

- Python 3.10+ (recommended)
- `streamlit`
- `groq`

## Installation

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the app

From the project directory:

```bash
streamlit run Nirnay.py
```

Then open the local URL shown in the terminal.

## Optional configuration

The app can use the Groq API key if provided via Streamlit secrets. Create a `.streamlit/secrets.toml` file with:

```toml
GROQ_API_KEY = "your_api_key_here"
```

If no API key is set, the app will still attempt to use the `groq` client with default credentials.

## Notes

- This project is intended as an AI-assisted clinical workflow tool, not a replacement for medical professionals.
- The app includes a medical disclaimer and requires the user to agree before continuing.
- The AI chat assistant is designed to answer medical-related questions only and to avoid general or non-medical topics.

## Usage overview

1. Fill in patient profile details and accept the disclaimer.
2. Save or load patient profiles if needed.
3. Proceed to analysis and optionally upload clinical images.
4. Use the chat assistant for follow-up medical queries.

## License

This repository does not include a license file; add one if needed for your project.
