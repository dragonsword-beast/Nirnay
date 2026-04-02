# Nirnay

A Streamlit-based clinical diagnostic workflow interface for patient intake, image review, and AI-assisted analysis.

## Overview

`Nirnay.py` implements a polished web dashboard for a clinical workflow experience. It includes:
- Patient intake and profile management
- Analysis and insights console
- AI chat/assistant interaction
- File upload support for images and clinical data
- Custom dark UI theme and responsive layout

## Features

- Interactive patient profile collection
- Insight dashboard with metrics and action cards
- AI assistant chat options for medical guidance
- Structured data and image upload workflow
- Custom CSS styling and polished visual design
- Upload and preview clinical images
- Remove individual uploaded images or clear all uploads
- Generate AI-assisted diagnostic summaries

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Current dependencies:
- `streamlit`
- `groq`

## Run locally

From the project directory, launch the app with:

```bash
streamlit run Nirnay.py
```

Open the local URL shown in the terminal to access the app.

## File structure

- `Nirnay.py` — main Streamlit application and UI logic
- `requirements.txt` — Python dependencies
- `README.md` — project documentation
- `893a2625-aa76-4993-af22-650fd069b640-8.png` — brand/logo image asset used in the UI
- `website code.txt` — backup or extra website code

## Notes

- The app uses inline CSS via `st.markdown` for custom styling.
- If you add more dependencies, update `requirements.txt` accordingly.
- Refresh the Streamlit app after code changes to see updates.

## License

Use this project under your preferred license or internal use policy.
