import streamlit as st
import html
import re
import time
import base64
import pathlib
from groq import Groq

logo_png_path = pathlib.Path(__file__).resolve().parent / "893a2625-aa76-4993-af22-650fd069b640-8.png"
logo_image_url = "https://cdn.creativefabrica.com/2020/07/17/Medicine-Logo-Graphics-4647232-1-580x386.jpg"

def _load_logo_html(path: pathlib.Path, remote_url: str, fallback_text: str = "Nirnay") -> str:
    if path.exists():
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f'<img class="brand-logo" src="data:image/png;base64,{data}" alt="Nirnay logo" />'
    if remote_url:
        return f'<img class="brand-logo" src="{html.escape(remote_url)}" alt="Nirnay logo" />'
    return f'<div class="brand-logo-fallback">{html.escape(fallback_text)}</div>'

logo_html = _load_logo_html(logo_png_path, logo_image_url)
icon_path = logo_image_url if logo_image_url else (str(logo_png_path) if logo_png_path.exists() else "nirnay.ico")

st.set_page_config(
    page_title="Nirnay | Clinical Diagnostic Workflow",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- THEME COLORS---
neutral_light = "#e8f3fc"
highlight_gold = "#f3c136"
surface_white = "#f5f7fb"
surface_frost = "#dde6f4"
primary_cyan = "#27c8f1"
primary_ink = "#1761c1"
border_ink = "#1f3042"
text_night = "#020617"
success_mint = "#22c55e"
warning_amber = "#eab308"
danger_crimson = "#dc2626"


st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {{
        --primary-color: #2563eb;
        --background-color: #ffffff;
        --surface-color: #f8fafc;
        --card-color: #ffffff;
        --border-color: #e2e8f0;
        --text-color: #1e293b;
        --text-muted: #64748b;
        --success-color: #22c55e;
        --warning-color: #eab308;
        --danger-color: #ef4444;
        --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
        --radius: 8px;
        --max-width: 1200px;
    }}

    * {{
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }}

    body, .stApp {{
        background: var(--background-color);
        color: var(--text-color);
        margin: 0;
        padding: 0;
    }}

    .block-container {{
        padding: 2rem 1rem;
        max-width: var(--max-width);
        margin: 0 auto;
    }}

    /* Hide Streamlit elements */
    #MainMenu, footer, .stDeployButton {{
        visibility: hidden !important;
    }}

    header {{
        display: none !important;
    }}

    /* Typography */
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-color);
        margin: 0 0 0.5rem 0;
        line-height: 1.2;
    }}

    .subtitle {{
        font-size: 1.1rem;
        color: var(--text-muted);
        margin: 0 0 2rem 0;
        line-height: 1.5;
    }}

    /* Cards */
    .card {{
        background: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
    }}

    .card-header {{
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin: 0 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* Stepper */
    .stepper {{
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }}

    .step {{
        padding: 0.75rem 1rem;
        border-radius: var(--radius);
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        color: var(--text-muted);
        font-size: 0.9rem;
        font-weight: 500;
        flex: 1;
        min-width: 120px;
        text-align: center;
    }}

    .step.active {{
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }}

    /* Results section */
    .result-section {{
        background: var(--card-color);
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 1.5rem;
        box-shadow: var(--shadow);
    }}

    /* Buttons */
    .stButton>button {{
        background: var(--primary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}

    .stButton>button:hover {{
        background: #1d4ed8 !important;
        transform: translateY(-1px);
    }}

    /* Form elements */
    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>select {{
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius) !important;
        padding: 0.75rem !important;
        background: var(--card-color) !important;
    }}

    /* File uploader */
    .stFileUploader {{
        border: 2px dashed var(--border-color) !important;
        border-radius: var(--radius) !important;
        padding: 1rem !important;
        background: var(--surface-color) !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: transparent;
    }}

    .stTabs [data-baseweb="tab-list"] [data-baseweb="tab"] {{
        background: transparent;
        border-radius: var(--radius) var(--radius) 0 0;
        padding: 0.75rem 1.5rem;
        border: 1px solid var(--border-color);
        border-bottom: none;
        color: var(--text-muted);
        font-weight: 500;
    }}

    .stTabs [data-baseweb="tab-list"] [aria-selected="true"] {{
        background: var(--card-color);
        color: var(--text-color);
        border-color: var(--border-color);
    }}

    .stTabs [data-baseweb="tab-panel"] {{
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 var(--radius) var(--radius);
        padding: 1.5rem;
        background: var(--card-color);
    }}

    /* Chat messages */
    .stChatMessage {{
        border: 1px solid var(--border-color);
        border-radius: var(--radius);
        padding: 1rem;
        margin-bottom: 0.5rem;
        background: var(--surface-color);
    }}

    /* Success/Warning messages */
    .stSuccess, .stWarning, .stError {{
        border-radius: var(--radius) !important;
        border: 1px solid var(--border-color) !important;
    }}

    /* Spinner */
    .stSpinner {{
        text-align: center;
        padding: 2rem;
    }}

    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .block-container {{
            padding: 1rem 0.5rem;
        }}

        .main-header {{
            font-size: 2rem;
        }}

        .stepper {{
            flex-direction: column;
        }}

        .step {{
            min-width: auto;
        }}

        .card {{
            padding: 1rem;
        }}
    }}
    </style>
        .custom-navbar {{
            padding: 0.75rem 0.75rem;
            border-radius: 12px;
        }}
        .main-header {{
            font-size: clamp(1.8rem, 7vw, 2.2rem);
        }}
        .subtitle {{
            font-size: clamp(0.85rem, 4vw, 0.95rem);
        }}
        .hero-trust-row {{
            flex-direction: column;
            gap: 0.5rem;
        }}
        .hero-trust-item {{
            padding: 0.75rem 0.9rem;
            font-size: 0.9rem;
            text-align: center;
        }}
        .feature-card {{
            padding: 1.25rem;
        }}
        .feature-title {{
            font-size: 0.95rem;
        }}
        .feature-copy {{
            font-size: 0.9rem;
        }}
        .stepper-step {{
            padding: 0.8rem 1rem;
            font-size: 0.9rem;
            min-height: 50px;
        }}
        .panel-title {{
            font-size: 1.1rem;
        }}
        .panel-subtitle {{
            font-size: 0.9rem;
        }}
        .stButton>button, .stButton>div>button, .stButton>div>div>button {{
            padding: 1.1rem 1.5rem !important;
            font-size: 1.05rem !important;
            min-height: 50px !important;
        }}
        .custom-footer {{
            padding: 1.25rem 0.75rem;
        }}
        .footer-credits p {{
            font-size: 0.9rem;
        }}
        .glass-card {{
            padding: 0.875rem;
        }}
        .card-header {{
            margin-bottom: 0.75rem;
        }}
        .profile-name {{
            font-size: 1rem;
        }}
        .profile-meta {{
            font-size: 0.9rem;
        }}
        .status-badge {{
            padding: 0.5rem 0.75rem;
            font-size: 0.8rem;
        }}
        .metric-pill {{
            padding: 0.875rem;
        }}
        .metric-pill strong {{
            font-size: 0.95rem;
        }}
        .metric-pill span {{
            font-size: 0.88rem;
        }}
        .assistant-title {{
            font-size: 1rem;
        }}
        .assistant-chip {{
            padding: 0.5rem 0.8rem;
            font-size: 0.85rem;
        }}
        .assistant-card {{
            padding: 0.875rem;
        }}
        .assistant-card h4 {{
            font-size: 0.95rem;
        }}
        .result-line {{
            font-size: 0.9rem;
        }}
        .upload-report-card {{
            width: 90vw;
            max-width: 300px;
        }}
    }}

    /* Improved visual hierarchy */
    .subtitle {{
        text-align: center;
        color: var(--secondary-text-color);
        font-size: clamp(1rem, 2.5vw, 1.1rem);
        font-weight: 400;
        margin-bottom: 1.75rem;
        opacity: 0.92;
    }}

    /* Responsive typography */
    @media (max-width: 768px) {{
        .main-header {{
            font-size: clamp(2rem, 6vw, 2.5rem);
        }}
        .subtitle {{
            font-size: clamp(0.9rem, 3vw, 1rem);
        }}
    }}

    .topbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1rem;
        padding: 0.8rem 1rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
    }}

    .stepper {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin-bottom: 1.75rem;
        padding: 0.75rem 0;
    }}

    .stepper-step {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.6rem;
        padding: 0.9rem 1rem;
        border-radius: 18px;
        background: rgba(255,255,255,0.06);
        border: 1px solid var(--border-color);
        color: var(--secondary-text-color);
        font-weight: 700;
        font-size: 0.98rem;
        text-align: center;
        min-height: 62px;
        transition: all 0.3s ease;
    }}

    .stepper-step.active {{
        background: linear-gradient(135deg, rgba(19, 71, 135, 0.24) 0%, rgba(11, 32, 58, 0.95) 100%);
        border-color: rgba(36, 141, 227, 0.45);
        color: var(--surface-white);
        box-shadow: 0 0 26px rgba(37, 200, 241, 0.18), 0 24px 48px rgba(0,0,0,0.22);
        animation: glowPulse 3.2s ease-in-out infinite;
    }}

    /* Mobile stepper */
    @media (max-width: 768px) {{
        .stepper {{
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }}
        .stepper-step {{
            min-height: 50px;
            padding: 0.7rem 0.8rem;
            font-size: 0.9rem;
        }}
    }}

    .stepper-step.completed {{
        color: {surface_white};
        background: rgba(37, 200, 241, 0.08);
        border-color: rgba(37, 200, 241, 0.18);
    }}

    .stepper-step.upcoming {{
        opacity: 0.75;
    }}

    .stepper-step span.status {{
        color: {primary_cyan};
        font-size: 0.82rem;
        font-weight: 600;
    }}

    @keyframes glowPulse {{
        0%, 100% {{
            box-shadow: 0 0 0 rgba(37, 200, 241, 0.0);
        }}
        50% {{
            box-shadow: 0 0 26px rgba(37, 200, 241, 0.18);
        }}
    }}

    .analysis-shell {{
        display: grid;
        gap: 1.25rem;
        margin-bottom: 1.6rem;
        padding: 1.4rem;
        background: rgba(7, 14, 28, 0.75);
        border: 1px solid rgba(37, 200, 241, 0.14);
        border-radius: 28px;
        box-shadow: 0 30px 90px rgba(0, 0, 0, 0.26);
        backdrop-filter: blur(18px);
    }}

    .analysis-header {{
        display: grid;
        gap: 1rem;
    }}

    .analysis-title-block h1 {{
        margin: 0;
        font-size: 2.3rem;
        line-height: 1.05;
        color: {surface_white};
        letter-spacing: 0.02em;
    }}

    .step-label {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.55rem 0.9rem;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        background: rgba(37, 200, 241, 0.12);
        color: {primary_cyan};
        border: 1px solid rgba(37, 200, 241, 0.2);
        width: fit-content;
    }}

    .page-guide {{
        margin: 0.75rem 0 0;
        color: rgba(229, 239, 255, 0.82);
        max-width: 740px;
        line-height: 1.75;
        font-size: 1rem;
    }}

    .patient-pill-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
    }}

    .patient-pill {{
        display: inline-flex;
        align-items: center;
        padding: 0.75rem 1rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: {surface_white};
        font-size: 0.92rem;
        letter-spacing: 0.01em;
    }}

    .analysis-meta-grid {{
        display: grid;
        grid-template-columns: 1fr minmax(260px, 340px);
        gap: 1rem;
        align-items: start;
    }}

    /* Mobile analysis grid */
    @media (max-width: 980px) {{
        .analysis-meta-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    .risk-card {{
        display: grid;
        gap: 0.85rem;
        padding: 1.25rem;
        border-radius: 24px;
        border: 1px solid rgba(37, 200, 241, 0.14);
        background: rgba(7, 14, 28, 0.88);
        box-shadow: 0 18px 40px rgba(0,0,0,0.18);
    }}

    .risk-label {{
        color: rgba(229, 239, 255, 0.84);
        font-size: 0.95rem;
        margin: 0;
    }}

    .risk-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 94px;
        padding: 0.65rem 0.95rem;
        border-radius: 999px;
        font-weight: 700;
        letter-spacing: 0.01em;
        color: #020617;
        background: linear-gradient(135deg, #27c8f1 0%, #1761c1 100%);
    }}

    .assistant-panel {{
        padding: 1.35rem;
        border-radius: 28px;
        background: rgba(9, 18, 35, 0.95);
        border: 1px solid rgba(37, 200, 241, 0.18);
        box-shadow: 0 24px 56px rgba(0,0,0,0.24);
        backdrop-filter: blur(20px);
    }}

    .assistant-panel.sticky {{
        position: sticky;
        top: 1.6rem;
    }}

    .assistant-title {{
        margin: 0 0 1rem;
        font-size: 1.3rem;
        color: {surface_white};
        letter-spacing: 0.01em;
    }}

    .assistant-chip-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }}

    .assistant-chip {{
        display: inline-flex;
        align-items: center;
        padding: 0.55rem 0.9rem;
        border-radius: 999px;
        background: rgba(37, 200, 241, 0.15);
        color: {surface_white};
        font-size: 0.92rem;
        font-weight: 600;
    }}

    .assistant-card {{
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
    }}

    .assistant-card h4 {{
        margin: 0 0 0.75rem;
        color: #d9eeff;
        font-size: 1rem;
    }}

    .assistant-card p,
    .assistant-card li {{
        color: rgba(228,236,249,0.88);
        line-height: 1.7;
        font-size: 0.95rem;
    }}

    .assistant-card ul {{
        margin: 0;
        padding-left: 1.2rem;
    }}

    .panel-card {{
        background: rgba(15, 29, 45, 0.96);
        border: 1px solid rgba(37, 200, 241, 0.14);
        border-radius: 24px;
        padding: 1.4rem;
        box-shadow: 0 18px 42px rgba(0,0,0,0.22);
        backdrop-filter: blur(16px);
        margin-bottom: 1.25rem;
    }}

    .panel-title {{
        margin: 0 0 0.75rem;
        color: {primary_cyan};
        font-size: 1.15rem;
        letter-spacing: 0.01em;
    }}

    .panel-subtitle {{
        margin: 0;
        color: rgba(229, 239, 255, 0.8);
        line-height: 1.7;
        font-size: 0.96rem;
    }}

    .field-note {{
        margin-top: 1rem;
        color: rgba(229, 239, 255, 0.72);
        font-size: 0.92rem;
    }}

    .upload-panel {{
        position: relative;
    }}

    .upload-panel::before {{
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(37, 200, 241, 0.08), rgba(51, 116, 206, 0.05));
        pointer-events: none;
    }}

    .action-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 1rem 1.2rem;
        margin-top: 1.25rem;
        border-radius: 22px;
        background: rgba(7, 14, 28, 0.92);
        border: 1px solid rgba(37, 200, 241, 0.14);
        box-shadow: 0 22px 55px rgba(0,0,0,0.28);
        position: sticky;
        bottom: 0;
        z-index: 12;
    }}

    .action-copy {{
        color: rgba(229, 239, 255, 0.86);
        font-size: 0.95rem;
        line-height: 1.6;
    }}

    .status-pill {{
        display: inline-flex;
        align-items: center;
        padding: 0.65rem 0.95rem;
        border-radius: 999px;
        background: rgba(37, 200, 241, 0.14);
        color: {surface_white};
        font-weight: 700;
        letter-spacing: 0.01em;
    }}

    .field-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 1rem;
    }}

    /* Mobile field grid */
    @media (max-width: 640px) {{
        .field-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    .symptom-panel {{
        background: rgba(22, 38, 62, 0.92);
        border: 1px solid rgba(37, 200, 241, 0.14);
        border-radius: 24px;
        padding: 1.25rem;
    }}

    .symptom-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.75rem;
    }}

    /* Mobile symptom grid */
    @media (max-width: 480px) {{
        .symptom-grid {{
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        }}
    }}

    .symptom-chip {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.85rem 1rem;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        color: rgba(229,239,255,0.88);
        background: rgba(255,255,255,0.04);
        transition: transform 0.22s ease, background 0.22s ease, border-color 0.22s ease;
        cursor: pointer;
    }}

    .symptom-chip:hover {{
        transform: translateY(-1px);
        border-color: rgba(37, 200, 241, 0.3);
        background: rgba(37, 200, 241, 0.08);
    }}

    .symptom-chip.selected {{
        background: rgba(37, 200, 241, 0.18);
        border-color: rgba(37, 200, 241, 0.28);
        color: #ffffff;
    }}

    @media (max-width: 980px) {{
        .analysis-meta-grid,
        .analysis-shell,
        .analysis-grid {{
            display: block;
        }}
        .action-bar {{
            flex-direction: column;
            align-items: stretch;
        }}
    }}

    .topbar-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .topbar-brand h1 {{
        margin: 0;
        font-size: 1.4rem;
        letter-spacing: 0.08em;
        color: {surface_white};
    }}

    .topbar-tagline {{
        color: {surface_frost};
        font-size: 0.95rem;
        margin: 0;
    }}

    .site-hero {{
        display: grid;
        gap: 1.2rem;
        background: linear-gradient(180deg, rgba(8,18,33,0.98), rgba(15,33,57,0.95));
        border: 1px solid rgba(79,209,197,0.16);
        border-radius: 32px;
        padding: 2.4rem;
        margin-bottom: 1.75rem;
        box-shadow: 0 28px 70px rgba(0,0,0,0.28);
        max-width: 1000px;
        margin-left: auto;
        margin-right: auto;
    }}

    /* Mobile hero */
    @media (max-width: 768px) {{
        .site-hero {{
            padding: 1.5rem 1rem;
            border-radius: 20px;
            margin: 0 1rem 1.5rem;
        }}
    }}

    @media (max-width: 480px) {{
        .site-hero {{
            padding: 1rem 0.75rem;
            margin: 0 0.5rem 1rem;
        }}
    }}

    .brand-header {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.55rem;
        width: 100%;
        flex-wrap: wrap;
    }}

    .brand-logo {{
        width: 88px;
        height: 88px;
        min-width: 88px;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(37, 200, 241, 0.24), rgba(23, 97, 193, 0.96));
        padding: 0.7rem;
        border: 1px solid rgba(79, 209, 197, 0.3);
        box-shadow: 0 16px 30px rgba(0,0,0,0.14);
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .brand-copy {{
        display: grid;
        gap: 0.2rem;
        max-width: 720px;
        justify-items: start;
        text-align: left;
    }}

    .brand-logo img {{
        width: 100%;
        height: 100%;
        border-radius: 18px;
        object-fit: contain;
    }}

    .brand-copy {{
        display: grid;
        gap: 0.35rem;
        max-width: 720px;
        justify-items: center;
    }}

    .site-hero > div:first-child {{
        max-width: 860px;
    }}

    .site-hero h1,
    .main-header {{
        margin: 0;
        color: {surface_white};
        font-size: clamp(2.8rem, 4vw, 4.2rem);
        line-height: 1.02;
        font-weight: 900;
        text-align: center;
    }}

    .site-hero p,
    .subtitle {{
        margin: 0;
        color: rgba(235, 247, 255, 0.88);
        font-size: 1.05rem;
        line-height: 1.75;
        text-align: center;
        max-width: 760px;
    }}

    .hero-actions {{
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }}

    /* Mobile hero actions */
    @media (max-width: 480px) {{
        .hero-actions {{
            flex-direction: column;
            align-items: center;
        }}
        .hero-primary-cta,
        .hero-secondary-cta {{
            width: 100%;
            max-width: 280px;
        }}
    }}

    .hero-primary-cta,
    .hero-secondary-cta {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 1rem 1.6rem;
        border-radius: 999px;
        font-weight: 700;
        letter-spacing: 0.01em;
        transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
        text-decoration: none;
    }}

    .hero-primary-cta {{
        background: linear-gradient(135deg, #05254e 0%, #0d4b8a 100%);
        color: #ffffff;
        box-shadow: 0 22px 46px rgba(5, 37, 78, 0.32);
    }}

    .hero-primary-cta:hover {{
        transform: translateY(-2px) scale(1.02);
        background: linear-gradient(135deg, #0a3f7d 0%, #2f75b2 100%);
        box-shadow: 0 28px 58px rgba(9, 57, 100, 0.34);
    }}

    .hero-secondary-cta {{
        background: rgba(8,32,60,0.14);
        color: rgba(236,242,255,0.95);
        border: 1px solid rgba(58, 96, 150, 0.36);
    }}

    .hero-secondary-cta:hover {{
        transform: translateY(-2px);
        background: rgba(16, 50, 85, 0.28);
        border-color: rgba(72, 112, 182, 0.54);
        color: #ffffff;
    }}

    .hero-trust-row {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.85rem;
        margin-top: 1rem;
    }}

    /* Mobile hero trust */
    @media (max-width: 640px) {{
        .hero-trust-row {{
            grid-template-columns: 1fr;
        }}
    }}

    .hero-trust-item {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.95rem 1rem;
        border-radius: 18px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: {surface_frost};
        font-size: 0.95rem;
    }}

    .profile-card {{
        background: rgba(255,255,255,0.05);
        border: 1px solid var(--border-color);
        border-radius: 28px;
        padding: 2rem;
        max-width: 980px;
        margin: 0 auto 1.75rem;
        box-shadow: 0 26px 64px rgba(0,0,0,0.24);
    }}

    /* Mobile profile card */
    @media (max-width: 768px) {{
        .profile-card {{
            padding: 1.5rem;
            border-radius: 20px;
            margin: 0 1rem 1.5rem;
        }}
    }}

    @media (max-width: 480px) {{
        .profile-card {{
            padding: 1rem;
            margin: 0 0.5rem 1rem;
        }}
    }}

    .profile-card .card-header {{
        margin-bottom: 1rem;
        font-size: 1.45rem;
        color: {primary_cyan};
    }}

    .profile-group {{
        display: grid;
        gap: 1rem;
        margin-top: 1rem;
    }}

    .profile-group h3 {{
        margin: 0;
        font-size: 1.1rem;
        color: {surface_white};
    }}

    .profile-group p {{
        margin: 0.5rem 0 0;
        color: {surface_frost};
        line-height: 1.7;
    }}

    .button-block {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.85rem;
        margin-top: 1.5rem;
    }}

    /* Mobile button block */
    @media (max-width: 480px) {{
        .button-block {{
            flex-direction: column;
            align-items: center;
        }}
    }}

    .stButton>button,
    .stButton>div>button,
    .stButton>div>div>button {{
        display: block !important;
        width: 100% !important;
        max-width: 420px !important;
        min-height: 56px;
        padding: 0.95rem 1.3rem !important;
        border-radius: 14px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease-in-out !important;
        background: linear-gradient(135deg, #06264e 0%, #0d4f8b 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        box-shadow: 0 20px 40px rgba(5, 38, 78, 0.30) !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.18) !important;
        cursor: pointer !important;
        transform: translateZ(0);
        backdrop-filter: blur(2px) !important;
    }}

    /* Mobile buttons */
    @media (max-width: 480px) {{
        .stButton>button,
        .stButton>div>button,
        .stButton>div>div>button {{
            min-height: 48px;
            padding: 0.8rem 1rem !important;
            font-size: 0.95rem !important;
            max-width: 100% !important;
        }}
    }}

    .stButton>button:hover,
    .stButton>div>button:hover,
    .stButton>div>div>button:hover {{
        background: linear-gradient(135deg, #113f78 0%, #3b79b6 100%) !important;
        box-shadow: 0 26px 54px rgba(15, 66, 110, 0.36) !important;
        transform: translateY(-1px) scale(1.02) !important;
    }}

    .stButton>button:active,
    .stButton>div>button:active,
    .stButton>div>div>button:active {{
        background: linear-gradient(135deg, #062249 0%, #0f3d78 100%) !important;
        box-shadow: 0 10px 18px rgba(6, 28, 55, 0.30) !important;
        transform: translateY(1px) scale(0.98) !important;
        opacity: 0.98 !important;
    }}

    .stButton>button[disabled],
    .stButton>div>button[disabled],
    .stButton>div>div>button[disabled] {{
        background: rgba(110,120,140,0.18) !important;
        color: rgba(255,255,255,0.75) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        transform: none !important;
        opacity: 0.72 !important;
        pointer-events: none !important;
    }}

    .stTextInput>div>div>input,
    .stTextInput>div>div>div>input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSearchInput"] input,
    .stSelectbox>div>div>select,
    div[data-testid="stSelectbox"] select,
    input[type="text"],
    input[type="number"],
    textarea,
    select {{
        background-color: rgba(12, 24, 39, 0.92) !important;
        color: #ffffff !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
    }}

    /* Mobile inputs */
    @media (max-width: 480px) {{
        .stTextInput>div>div>input,
        .stTextInput>div>div>div>input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSearchInput"] input,
        .stSelectbox>div>div>select,
        div[data-testid="stSelectbox"] select,
        input[type="text"],
        input[type="number"],
        textarea,
        select {{
            padding: 0.8rem !important;
            font-size: 0.95rem !important;
        }}
    }}

    input::placeholder,
    textarea::placeholder {{
        color: rgba(255,255,255,0.6) !important;
    }}

    .stCheckbox>div>label {{
        display: block;
        width: 100%;
        color: var(--surface-white);
        font-weight: 600;
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.75rem;
        font-size: 0.98rem;
    }}

    /* Mobile checkboxes */
    @media (max-width: 480px) {{
        .stCheckbox>div>label {{
            padding: 0.8rem;
            font-size: 0.9rem;
        }}
    }}

    .stCheckbox>div>label:hover {{
        background: rgba(79, 209, 197, 0.1);
        transform: translateY(-1px);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(18, 36, 55, 0.9);
        border-radius: 16px;
        padding: 0.55rem;
        display: flex;
        overflow-x: auto;
        white-space: nowrap;
        gap: 0.55rem;
        -webkit-overflow-scrolling: touch;
    }}

    /* Mobile tabs */
    @media (max-width: 480px) {{
        .stTabs [data-baseweb="tab-list"] {{
            padding: 0.4rem;
            gap: 0.3rem;
        }}
    }}

    .hero-stat {{
        display: grid;
        gap: 0.9rem;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1rem;
    }}

    .hero-stat h3 {{
        margin: 0;
        color: #27c8f1;
        font-size: 1rem;
        font-weight: 700;
    }}

    .hero-stat p {{
        margin: 0;
        color: #f5f7fb;
        line-height: 1.55;
        opacity: 0.95;
        font-size: 0.95rem;
    }}

    .hero-metric {{
        padding: 0.8rem 1rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
    }}

    .hero-metric strong {{
        color: #1761c1;
        font-size: 1.15rem;
        display: block;
    }}

    .hero-metric span {{
        color: #dde6f4;
        font-size: 0.88rem;
    }}

    .section-card {{
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 22px;
        padding: 1.1rem;
        margin-top: 1rem;
    }}

    .disclaimer-banner {{
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 22px;
        padding: 1rem 1.15rem;
        margin: 1rem 0 1.5rem;
        color: #f5f7fb;
        line-height: 1.55;
        box-shadow: 0 16px 32px rgba(0,0,0,0.14);
    }}

    .disclaimer-banner strong {{
        color: #27c8f1;
    }}

    .hint-box {{
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 22px;
        padding: 1.15rem 1.2rem;
        margin: 1rem 0;
        color: #f5f7fb;
        line-height: 1.6;
    }}

    .hint-box strong {{
        color: #27c8f1;
    }}

    .section-card h3 {{
        margin-top: 0;
        margin-bottom: 0.9rem;
        color: #f5f7fb;
        font-size: 1.2rem;
        font-weight: 700;
    }}

    .section-row {{
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }}

    .section-pill {{
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 999px;
        padding: 0.7rem 1rem;
        color: #f5f7fb;
        font-size: 0.93rem;
        opacity: 0.92;
    }}

    .analysis-banner {{
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(260px, 0.95fr);
        gap: 1rem;
        margin-bottom: 1.2rem;
        padding: 1rem;
        background: rgba(5, 12, 24, 0.92);
        border: 1px solid rgba(79, 209, 197, 0.16);
        border-radius: 26px;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(16px);
    }}

    .analysis-summary {{
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 1.5rem;
        min-height: 220px;
        box-shadow: inset 0 0 0 1px rgba(79, 209, 197, 0.05);
    }}

    .analysis-summary .card-header {{
        margin-top: 0;
        color: #27c8f1;
        font-size: 1.35rem;
        letter-spacing: 0.02em;
    }}

    .analysis-summary p {{
        margin: 0.8rem 0 1rem;
        color: #dde6f4;
        line-height: 1.75;
    }}

    .analysis-summary ul {{
        margin: 0;
        padding-left: 1.3rem;
        color: #f5f7fb;
        line-height: 1.85;
        list-style: disc inside;
    }}

    .analysis-summary li {{
        margin-bottom: 0.85rem;
    }}

    .analysis-sidebar-card {{
        background: rgba(12, 24, 41, 0.96);
        border: 1px solid rgba(79, 209, 197, 0.18);
        border-radius: 24px;
        padding: 1.5rem;
        min-height: 220px;
        display: grid;
        gap: 0.8rem;
        box-shadow: 0 20px 44px rgba(0,0,0,0.24);
    }}

    .analysis-sidebar-card h3 {{
        margin: 0;
        color: #1761c1;
        font-size: 1.2rem;
        letter-spacing: 0.02em;
    }}

    .analysis-sidebar-card p {{
        margin: 0.65rem 0;
        color: rgba(255,255,255,0.88);
        line-height: 1.75;
    }}

    .analysis-sidebar-card strong {{
        color: #f5f7fb;
    }}

    .card {{
        background: rgba(20, 38, 58, 0.92);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1.75rem;
        margin: 1rem 0;
        box-shadow: 0 16px 38px rgba(0,0,0,0.24);
        backdrop-filter: blur(14px);
    }}

    .card-header {{
        color: #27c8f1;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(79, 209, 197, 0.24);
        padding-bottom: 0.65rem;
    }}

    .info-card {{
        background: rgba(19, 32, 49, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}

    .info-card h2 {{
        color: #1761c1;
        margin-bottom: 0.5rem;
    }}

    .info-card ul {{
        margin: 0.75rem 0 0 1.2rem;
        color: #f5f7fb;
        line-height: 1.75;
    }}

    .stTextInput>div>div>input, .stSelectbox>div>div>select {{
        background-color: rgba(12, 24, 39, 0.9);
        color: #f5f7fb;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 0.85rem;
        box-shadow: inset 0 1px 5px rgba(0,0,0,0.22);
    }}

    .stCheckbox>div>label {{
        display: block;
        width: 100%;
        color: #f5f7fb;
        font-weight: 500;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
        transition: background 0.2s ease, transform 0.2s ease;
    }}

    .stCheckbox>div>label:hover {{
        background: rgba(79, 209, 197, 0.08);
        transform: translateY(-1px);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(18, 36, 55, 0.9);
        border-radius: 16px;
        padding: 0.55rem;
        display: flex;
        overflow-x: auto;
        white-space: nowrap;
        gap: 0.55rem;
        -webkit-overflow-scrolling: touch;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
        height: 8px;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {{
        background: rgba(79, 209, 197, 0.4);
        border-radius: 999px;
    }}

    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {{
        background: rgba(255,255,255,0.05);
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255, 255, 255, 0.04);
        color: #f5f7fb;
        border-radius: 12px;
        padding: 0.85rem 1.4rem;
        font-weight: 600;
        min-width: 140px;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #27c8f1 0%, #1761c1 100%);
        color: #020617 !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.28);
    }}

    .patient-info {{
        background: rgba(7, 16, 28, 0.96);
        border: 1px solid rgba(79, 209, 197, 0.16);
        color: #f5f7fb;
        padding: 1rem 1.25rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 700;
        margin: 1rem 0;
    }}

    .disclaimer-text {{
        line-height: 1.75;
        color: #dde6f4;
        user-select: none;
    }}

    .disclaimer-text strong {{
        color: #27c8f1;
    }}

    .dashboard-overview {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }}

    .dashboard-tile {{
        background: rgba(15, 29, 45, 0.95);
        border: 1px solid rgba(79, 209, 197, 0.14);
        border-radius: 20px;
        padding: 1.4rem;
        min-height: 160px;
        box-shadow: 0 14px 30px rgba(0,0,0,0.18);
    }}

    .dashboard-tile h3 {{
        margin-top: 0;
        margin-bottom: 0.9rem;
        color: #27c8f1;
        font-size: 1.1rem;
    }}

    .dashboard-tile p {{
        margin: 0.45rem 0;
        color: #f5f7fb;
        opacity: 0.92;
        line-height: 1.7;
    }}

    .result-card {{
        background: rgba(12, 24, 39, 0.95);
        border: 1px solid rgba(79, 209, 197, 0.18);
        border-radius: 24px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 22px 60px rgba(0,0,0,0.28);
    }}

    .analysis-report-box {{
        background: linear-gradient(135deg, rgba(13, 31, 48, 0.96), rgba(5, 12, 24, 0.92));
        border: 1px solid rgba(79, 209, 197, 0.24);
        border-radius: 28px;
        padding: 2rem;
        margin: 1.5rem auto;
        max-width: 1140px;
        box-shadow: 0 28px 90px rgba(0, 0, 0, 0.32);
        backdrop-filter: blur(18px);
    }}

    .report-header {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .report-title {{
        color: #27c8f1;
        font-size: 2rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 0.02em;
    }}

    .report-subtitle {{
        color: #dde6f4;
        font-size: 1rem;
        margin: 0.35rem 0 0;
        line-height: 1.7;
    }}

    .report-badge {{
        padding: 0.95rem 1.15rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        color: #f5f7fb;
        font-size: 0.95rem;
        font-weight: 600;
        white-space: nowrap;
    }}

    .upload-report-hover {{
        position: relative;
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }}

    .upload-report-trigger {{
        cursor: pointer;
        font-weight: 700;
        color: #76d7ff;
        text-decoration: underline;
    }}

    .upload-report-card {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        top: 140%;
        left: 0;
        width: 360px;
        max-width: calc(100vw - 3rem);
        padding: 1rem 1.1rem;
        border-radius: 22px;
        background: rgba(8, 18, 34, 0.96);
        border: 1px solid rgba(37, 200, 241, 0.22);
        box-shadow: 0 22px 48px rgba(0, 0, 0, 0.38);
        transition: all 0.2s ease;
        z-index: 999;
        line-height: 1.65;
        color: #f5f8ff;
        pointer-events: none;
    }}

    .upload-report-hover:hover .upload-report-card {{
        visibility: visible;
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }}

    .result-body {{
        display: grid;
        gap: 0.9rem;
    }}

    .result-line {{
        display: block;
        padding: 1rem 1.1rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(10, 18, 32, 0.85);
        color: #f5f7fb;
        line-height: 1.65;
        font-size: 0.98rem;
        white-space: pre-wrap;
    }}

    .result-line.critical {{
        border-color: rgba(255, 94, 94, 0.35);
        background: rgba(95, 15, 15, 0.55);
    }}

    .result-line.alert {{
        border-color: rgba(255, 161, 60, 0.35);
        background: rgba(86, 55, 14, 0.45);
    }}

    .result-line.warning {{
        border-color: rgba(255, 214, 80, 0.35);
        background: rgba(86, 79, 27, 0.40);
    }}

    .result-line.ok {{
        border-color: rgba(86, 214, 166, 0.30);
        background: rgba(14, 38, 41, 0.58);
    }}

    .result-line.heading {{
        border: none;
        background: transparent;
        color: #27c8f1;
        font-weight: 700;
        font-size: 1.02rem;
        padding-left: 0;
    }}

    .footer {{
        text-align: center;
        color: #dde6f4;
        opacity: 0.84;
        margin-top: 3rem;
        padding-top: 2.5rem;
        border-top: 1px solid rgba(255,255,255,0.08);
    }}

    @media (max-width: 980px) {{
        .block-container {{
            padding: 1rem 0.9rem;
            max-width: 100%;
            margin: 0 auto;
        }}

        .site-hero,
        .hero-card,
        .analysis-banner,
        .summary-card,
        .card,
        .info-card,
        .result-card,
        .analysis-summary,
        .analysis-sidebar-card,
        .profile-card {{
            width: 100%;
            padding: 1rem;
            margin: 0 0 1rem;
        }}

        .site-hero {{
            padding: 1.5rem;
        }}

        .stat-grid,
        .feature-grid {{
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        }}

        .stTextInput>div>div>input,
        .stTextInput>div>div>div>input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stSearchInput"] input,
        .stSelectbox>div>div>select,
        div[data-testid="stSelectbox"] select {{
            width: 100%;
            font-size: 1rem;
        }}

        .stCheckbox>div>label {{
            width: 100%;
            font-size: 1rem;
        }}
    }}

    @media (max-width: 640px) {{
        .block-container {{
            padding: 0.9rem 0.75rem;
        }}

        .main-header {{
            font-size: 2.1rem;
        }}

        .subtitle {{
            font-size: 0.98rem;
        }}

        .site-hero,
        .hero-card,
        .analysis-banner {{
            gap: 1rem;
        }}

        .feature-grid,
        .stat-grid {{
            grid-template-columns: 1fr;
        }}

        .section-title {{
            font-size: 1.35rem;
            margin-top: 1.5rem;
        }}

        .button-block {{
            width: 100%;
        }}

        /* Premium dashboard theme */
        .stApp {{
            background: radial-gradient(circle at top left, #061323 0%, #051426 38%, #030f1e 100%);
            color: #e8faff;
        }}

        .block-container {{
            background: rgba(6, 14, 26, 0.92);
            border: 1px solid rgba(24, 109, 171, 0.18);
            box-shadow: 0 32px 96px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(26px);
            border-radius: 26px;
            padding: 2rem 2.2rem;
        }}

        .main-header {{
            color: #d4f5ff;
            text-shadow: 0 0 24px rgba(60, 190, 245, 0.16);
            letter-spacing: 0.02em;
        }}

        .subtitle {{
            color: rgba(225, 243, 255, 0.78);
            line-height: 1.75;
        }}

        .glass-card {{
            background: rgba(10, 20, 37, 0.86);
            border: 1px solid rgba(58, 152, 224, 0.18);
            border-radius: 24px;
            box-shadow: 0 26px 74px rgba(8, 22, 46, 0.30);
            backdrop-filter: blur(20px);
            transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
            overflow: hidden;
        }}

        .glass-card:hover {{
            transform: translateY(-3px) scale(1.004);
            border-color: rgba(36, 200, 255, 0.28);
            box-shadow: 0 34px 98px rgba(36, 148, 222, 0.22);
        }}

        .glass-card .card-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.1rem;
            color: #a0f4ff;
            font-size: 1.38rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }}

        .section-icon {{
            width: 42px;
            height: 42px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            background: rgba(38, 205, 255, 0.16);
            color: #c9f5ff;
            font-size: 1.1rem;
        }}

        .profile-row {{
            display: block;
            gap: 1rem;
        }}

        .avatar {{
            width: 76px;
            height: 76px;
            border-radius: 24px;
            display: grid;
            place-items: center;
            font-size: 1.65rem;
            font-weight: 800;
            color: #ffffff;
            background: linear-gradient(135deg, rgba(54, 200, 255, 0.92), rgba(124, 79, 252, 0.86));
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.16), 0 18px 38px rgba(32, 131, 218, 0.22);
        }}

        .profile-name {{
            font-size: 1.55rem;
            font-weight: 800;
            color: #ffffff !important;
            margin-bottom: 0.22rem;
        }}

        .profile-meta {{
            color: #ffffff !important;
            font-size: 0.98rem;
            line-height: 1.65;
        }}

        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.55rem 0.95rem;
            border-radius: 999px;
            background: rgba(37, 200, 241, 0.14);
            color: #ffffff !important;
            border: 1px solid rgba(37, 200, 241, 0.22);
            font-size: 0.88rem;
            font-weight: 700;
            margin-top: 0.85rem;
        }}

        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.92rem;
            margin-top: 1.35rem;
        }}

        .metric-pill {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 1rem 1rem;
        }}

        .metric-pill strong {{
            display: block;
            color: #ffffff !important;
            font-size: 1.05rem;
            margin-bottom: 0.3rem;
        }}

        .metric-pill span {{
            color: #ffffff !important;
            font-size: 0.92rem;
            line-height: 1.65;
        }}

        .dashboard-shell {{
            display: grid;
            gap: 1.4rem;
            animation: fadeInUp 0.84s ease both;
        }}

        .dashboard-top-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr);
            gap: 1.2rem;
        }}

        .insights-grid {{
            display: grid;
            gap: 0.9rem;
            margin-top: 1rem;
        }}

        .insight-item {{
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.9rem;
            align-items: center;
            padding: 0.95rem 1rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .insight-icon {{
            width: 44px;
            height: 44px;
            display: grid;
            place-items: center;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(43, 210, 255, 0.16), rgba(110, 85, 255, 0.16));
            color: #b6f6ff;
            font-size: 1.1rem;
        }}

        .insight-item strong {{
            color: #ffffff;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        }}

        .insight-item p {{
            margin: 0;
            color: rgba(241,248,255,0.78);
            font-size: 0.95rem;
            line-height: 1.65;
        }}

        .data-card, .notes-card, .action-card {{
            background: rgba(11, 20, 36, 0.82);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 24px;
            padding: 1.4rem;
            box-shadow: 0 20px 50px rgba(8, 18, 36, 0.24);
            margin-top: 1rem;
        }}

        .data-card h3,
        .notes-card h3,
        .action-card h3 {{
            margin-top: 0;
            margin-bottom: 0.9rem;
            color: #d8f7ff;
            font-size: 1.25rem;
        }}

        .data-card ul,
        .notes-card ul {{
            margin: 0.9rem 0 0 1.2rem;
            padding-left: 1.1rem;
            color: rgba(232,245,255,0.9);
            line-height: 1.8;
        }}

        .data-card li,
        .notes-card li {{
            margin-bottom: 0.85rem;
            font-size: 0.96rem;
        }}

        .progress-group {{
            display: grid;
            gap: 0.85rem;
            margin-top: 1rem;
        }}

        .progress-label {{
            display: flex;
            justify-content: space-between;
            color: rgba(242,250,255,0.76);
            font-size: 0.94rem;
            margin-bottom: 0.32rem;
        }}

        .progress-bar {{
            height: 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
        }}

        .progress-fill {{
            height: 100%;
            width: 72%;
            border-radius: 999px;
            background: linear-gradient(135deg, #2bd4ff 0%, #9866ff 100%);
            box-shadow: 0 0 22px rgba(46, 206, 255, 0.22);
        }}

        .notes-card details {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-top: 0.95rem;
        }}

        .notes-card summary {{
            cursor: pointer;
            font-size: 1rem;
            font-weight: 700;
            color: #ffffff;
            list-style: none;
        }}

        .notes-card summary::marker {{
            color: rgba(37,200,241,0.9);
        }}

        .action-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-top: 1rem;
        }}

        .stButton>button,
        .stButton>div>button,
        .stButton>div>div>button {{
            transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease !important;
        }}

        .stButton>button:hover,
        .stButton>div>button:hover,
        .stButton>div>div>button:hover {{
            box-shadow: 0 24px 62px rgba(46, 170, 232, 0.28) !important;
            transform: translateY(-2px) scale(1.01) !important;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(18px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    }}

    /* Custom Navbar */
    .custom-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(13, 31, 48, 0.95);
        border-bottom: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
        position: sticky;
        top: 0;
        z-index: 1000;
    }}

    .navbar-brand {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary-color);
    }}

    .navbar-nav {{
        display: flex;
        gap: 1rem;
    }}

    .nav-btn {{
        background: transparent;
        border: 1px solid var(--border-color);
        color: var(--secondary-text-color);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        font-weight: 500;
        cursor: pointer;
    }}

    .nav-btn:hover {{
        background: rgba(37, 200, 241, 0.1);
        border-color: rgba(37, 200, 241, 0.3);
        color: var(--primary-color);
    }}

    .nav-btn.active {{
        background: rgba(37, 200, 241, 0.2);
        border-color: rgba(37, 200, 241, 0.5);
        color: var(--primary-color);
    }}

    /* Mobile navbar */
    @media (max-width: 768px) {{
        .custom-navbar {{
            padding: 0.75rem 1rem;
        }}
        .navbar-brand {{
            font-size: 1.25rem;
        }}
        .navbar-nav {{
            gap: 0.5rem;
        }}
        .nav-btn {{
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }}
    }}

    /* Custom Footer */
    .custom-footer {{
        background: rgba(13, 31, 48, 0.95);
        border-top: 1px solid var(--border-color);
        padding: 2rem 2rem 1rem;
        margin-top: 3rem;
        backdrop-filter: blur(10px);
    }}

    .footer-content {{
        max-width: 1200px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 2rem;
        align-items: start;
    }}

    .footer-links {{
        display: flex;
        gap: 2rem;
        flex-wrap: wrap;
    }}

    .footer-links a {{
        color: var(--secondary-text-color);
        text-decoration: none;
        transition: color 0.3s ease;
    }}

    .footer-links a:hover {{
        color: var(--primary-color);
    }}

    .footer-credits {{
        text-align: right;
    }}

    .footer-credits p {{
        margin: 0.5rem 0;
        color: var(--secondary-text-color);
        font-size: 0.9rem;
    }}

    /* Mobile footer */
    @media (max-width: 768px) {{
        .custom-footer {{
            padding: 1.5rem 1rem 1rem;
        }}
        .footer-content {{
            grid-template-columns: 1fr;
            gap: 1rem;
            text-align: center;
        }}
        .footer-links {{
            justify-content: center;
            gap: 1rem;
        }}
        .footer-credits {{
            text-align: center;
        }}
    }}

    /* Global responsive column support */
    .stColumns {{
        display: grid !important;
        grid-template-columns: repeat(12, minmax(0, 1fr)) !important;
        gap: 1rem !important;
        width: 100%;
    }}
    .stColumns > div {{
        min-width: 0;
    }}
    @media (max-width: 980px) {{
        .stColumns {{
            grid-template-columns: 1fr !important;
        }}
    }}

    /* Profile form grid */
    .profile-form-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 1rem;
    }}

    @media (max-width: 980px) {{
        .profile-form-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    /* Analysis layout responsive */
    .analysis-layout {{
        display: grid;
        grid-template-columns: 7fr 3fr;
        gap: 1rem;
    }}

    @media (max-width: 980px) {{
        .analysis-layout {{
            display: block;
        }}
    }}

    /* Improved visual hierarchy */
    .section-heading {{
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--primary-color);
    }}

    .subsection-heading {{
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--secondary-text-color);
    }}

    .card-section {{
        margin-bottom: 2rem;
    }}

    /* Theme-aware colors */
    .primary-text {{
        color: var(--primary-color);
    }}

    .secondary-text {{
        color: var(--secondary-text-color);
    }}

    .surface-bg {{
        background: var(--card-background);
    }}

    .border {{
        border-color: var(--border-color);
    }}

    /* Responsive button grids */
    .responsive-button-grid {{
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }}
    .responsive-button-grid > div {{
        flex: 1;
        min-width: 200px;
    }}
    @media (max-width: 680px) {{
        .responsive-button-grid {{
            flex-direction: column;
        }}
        .responsive-button-grid > div {{
            min-width: unset;
        }}
    }}

    .responsive-download-grid {{
        display: flex;
        justify-content: flex-end;
        margin-top: 1rem;
    }}

    .responsive-action-grid {{
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }}
    .responsive-action-grid > div {{
        flex: 1;
        min-width: 150px;
    }}
    @media (max-width: 680px) {{
        .responsive-action-grid {{
            flex-direction: column;
        }}
        .responsive-action-grid > div {{
            min-width: unset;
        }}
    }}

    .responsive-chat-mode-grid {{
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
    }}
    .responsive-chat-mode-grid > div {{
        flex: 1;
    }}
    @media (max-width: 680px) {{
        .responsive-chat-mode-grid {{
            flex-direction: column;
        }}
    }}

    .responsive-suggestion-grid {{
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }}
    .responsive-suggestion-grid > div {{
        flex: 1;
        min-width: 200px;
    }}
    @media (max-width: 680px) {{
        .responsive-suggestion-grid {{
            flex-direction: column;
        }}
        .responsive-suggestion-grid > div {{
            min-width: unset;
        }}
    }}

    .responsive-assistant-grid {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }}
    .responsive-assistant-grid > div {{
        flex: 1;
    }}
    @media (max-width: 680px) {{
        .responsive-assistant-grid {{
            flex-direction: column;
        }}
    }}

    .responsive-action-bar-grid {{
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 0.5rem;
    }}
    .responsive-action-bar-grid > div {{
        flex: 1;
        min-width: 120px;
    }}
    @media (max-width: 680px) {{
        .responsive-action-bar-grid {{
            flex-direction: column;
        }}
        .responsive-action-bar-grid > div {{
            min-width: unset;
        }}
    }}

    .responsive-image-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }}
    @media (max-width: 680px) {{
        .responsive-image-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

def render_footer():
    st.markdown(
        """
        <footer class="footer">
            Created with passion by Aarko Batabyal & Saptak Bhattacharjee
        </footer>
        """,
        unsafe_allow_html=True,
    )

# ------------ Pages -------------
if "page" not in st.session_state:
    st.session_state.page = "profile"
page = st.session_state.page

if "chat_history_medical" not in st.session_state:
    st.session_state.chat_history_medical = []
if "chat_history_quick" not in st.session_state:
    st.session_state.chat_history_quick = []

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""
if "patient_age" not in st.session_state:
    st.session_state.patient_age = ""
if "patient_gender" not in st.session_state:
    st.session_state.patient_gender = ""
if "agree_disclaimer" not in st.session_state:
    st.session_state.agree_disclaimer = False
if "saved_profiles" not in st.session_state:
    st.session_state.saved_profiles = []
if "selected_saved_profile" not in st.session_state:
    st.session_state.selected_saved_profile = ""
if "profile_saved" not in st.session_state:
    st.session_state.profile_saved = False
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []
if "uploaded_image_report" not in st.session_state:
    st.session_state.uploaded_image_report = ""
if "manual_symptoms" not in st.session_state:
    st.session_state.manual_symptoms = ""

if "last_button_click" not in st.session_state:
    st.session_state.last_button_click = {"key": None, "time": 0.0}

def click_debounced(key, threshold=0.8):
    now = time.time()
    last = st.session_state.last_button_click
    if last.get("key") == key and now - last.get("time", 0.0) < threshold:
        return False
    st.session_state.last_button_click = {"key": key, "time": now}
    return True


def set_page(target):
    st.session_state.page = target
    st.rerun()


def remove_uploaded_image(index):
    images = st.session_state.uploaded_images
    if 0 <= index < len(images):
        st.session_state.uploaded_images = [img for idx, img in enumerate(images) if idx != index]
        st.session_state.uploaded_image_report = ""


def clear_uploaded_images():
    st.session_state.uploaded_images = []
    st.session_state.uploaded_image_report = ""


def save_profile():
    profile = {
        "name": st.session_state.patient_name.strip(),
        "age": st.session_state.patient_age.strip(),
        "gender": st.session_state.patient_gender,
    }
    if profile["name"] and profile["age"] and profile["gender"]:
        label = f"{profile['name']} · {profile['age']} · {profile['gender']}"
        if label not in [f"{p['name']} · {p['age']} · {p['gender']}" for p in st.session_state.saved_profiles]:
            st.session_state.saved_profiles.append(profile)
        st.session_state.profile_saved = True
    st.rerun()


def load_saved_profile():
    label = st.session_state.selected_saved_profile
    for p in st.session_state.saved_profiles:
        if f"{p['name']} · {p['age']} · {p['gender']}" == label:
            st.session_state.patient_name = p["name"]
            st.session_state.patient_age = p["age"]
            st.session_state.patient_gender = p["gender"]
            break
    st.rerun()


def continue_to_analysis():
    set_page("analysis")


def reset_profile():
    st.session_state.patient_name = ""
    st.session_state.patient_age = ""
    st.session_state.patient_gender = ""
    st.session_state.agree_disclaimer = False
    st.rerun()


def render_navbar():
    current_page = st.session_state.get("page", "profile")
    
    nav_html = f'''
    <nav class="custom-navbar">
        <div class="navbar-brand">{logo_html}<span>Nirnay</span></div>
        <div class="navbar-nav">
            <button class="nav-btn {'active' if current_page == 'profile' else ''}" onclick="javascript:void(0)">Home</button>
            <button class="nav-btn {'active' if current_page == 'analysis' else ''}" onclick="javascript:void(0)">Analysis</button>
            <button class="nav-btn {'active' if current_page == 'chat' else ''}" onclick="javascript:void(0)">Chat</button>
        </div>
    </nav>
    '''
    
    st.markdown(nav_html, unsafe_allow_html=True)


def render_custom_footer():
    st.markdown(
        """
        <footer class="custom-footer">
            <div class="footer-content">
                <div class="footer-links">
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Contact Us</a>
                    <a href="#">About</a>
                </div>
                <div class="footer-credits">
                    <p>&copy; 2024 Nirnay. Created with passion by Aarko Batabyal & Saptak Bhattacharjee. All rights reserved.</p>
                    <p>Empowering healthcare through AI-assisted diagnostics.</p>
                </div>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def back_to_analysis():
    set_page("analysis")


def request_analysis():
    st.session_state.analysis_requested = True


def launch_chat(mode=None):
    if mode is None:
        mode = (
            "medical" if st.session_state.get("chat_choice") == "Medical Assistant" else "quick"
        )
    st.session_state.chat_mode = mode
    st.session_state.page = "chat"

# ------------ Disclaimer -------------

if page == "profile":
    render_navbar()
    # Mobile-first hero landing layout for the initial profile screen.
    st.markdown("<div id='page-top'></div>", unsafe_allow_html=True)
    st.markdown("<script>window.scrollTo({top:0,behavior:'auto'});</script>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="stepper">
            <div class="stepper-step active"><span class="status">Step 1 of 3</span>Profile</div>
            <div class="stepper-step upcoming"><span class="status">Next</span>Analysis</div>
            <div class="stepper-step upcoming"><span class="status">Future</span>Chat</div>
        </div>
        <div class="site-hero">
            <div class="brand-header">
                {logo_html}
                <div class="brand-copy">
                    <h1 class="main-header">Nirnay</h1>
                    <p class="subtitle">World's Hope, Health's Future</p>
                </div>
            </div>
            <div class="hero-actions">
                <a class="hero-primary-cta" href="#profile-section">Start Assessment</a>
                <a class="hero-secondary-cta" href="#profile-section">Review patient intake</a>
            </div>
            <div class="hero-trust-row">
                <div class="hero-trust-item">🤖 AI-assisted, not a doctor</div>
                <div class="hero-trust-item">🔒 Secure by design</div>
                <div class="hero-trust-item">⚡ Fast clinical workflow</div>
            </div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-title">Structured clinical intake</div>
                    <div class="feature-copy">Capture patient vitals, symptoms, and diagnostic signals in one organized workflow.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">AI-driven insights</div>
                    <div class="feature-copy">Generate concise diagnostic guidance, risk flags, and follow-up suggestions.</div>
                </div>
                <div class="feature-card">
                    <div class="feature-title">Image review support</div>
                    <div class="feature-copy">Upload scans and photos for image-aware analysis and richer clinical context.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="disclaimer-banner">
            <div><strong>⚠️ Medical disclaimer</strong> This is an AI-assisted clinical workflow, not a clinical diagnosis tool. Please read the full disclaimer before continuing.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Read the full medical disclaimer", expanded=False):
        st.markdown(
            """
            <div class="disclaimer-text">
                <strong>IMPORTANT NOTICE:</strong><br>
                This diagnostic tool is designed to ASSIST and ENHANCE medical sciences.
                It is NOT a replacement for professional medical diagnosis, treatment, or advice from a qualified healthcare provider.
                <ul>
                    <li>All diagnostic findings and insights provided by this tool must be CORRELATED with a qualified physician or medical specialist.</li>
                    <li>Users should NOT rely solely on this tool for medical decisions.</li>
                    <li>Always consult your doctor before making any healthcare decisions based on this tool's output.</li>
                    <li>This tool is for educational and informational purposes only.</li>
                    <li>In case of medical emergencies, seek immediate professional medical attention.</li>
                </ul>
                <p>By proceeding, you acknowledge and accept full responsibility for your medical decisions and agree to consult with healthcare professionals regarding all diagnostic findings.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="glass-card profile-card" id="profile-section">
            <div class="card-header"><span class="section-icon">👤</span> Patient profile</div>
            <div class="profile-row">
                <div>
                    <div class="profile-name">Patient intake</div>
                    <div class="profile-meta">Complete the patient's core details to launch the diagnostic workup.</div>
                    <div class="status-badge">Ready to assess</div>
                </div>
            </div>
            <div class="metrics-grid">
                <div class="metric-pill">
                    <strong>Profile readiness</strong>
                    <span>{'Complete' if st.session_state.patient_name and st.session_state.patient_age and st.session_state.patient_gender else 'Pending details'}</span>
                </div>
                <div class="metric-pill">
                    <strong>Saved workflows</strong>
                    <span>{len(st.session_state.saved_profiles)} saved profiles</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    age_value = int(st.session_state.patient_age) if str(st.session_state.patient_age).isdigit() else 0
    
    st.markdown('<div class="profile-form-grid">', unsafe_allow_html=True)
    st.session_state.patient_name = st.text_input(
        "👤 Full name",
        value=st.session_state.patient_name,
        placeholder="e.g. John Doe",
    )
    st.session_state.patient_age = str(
        st.number_input(
            "🎂 Age",
            min_value=0,
            max_value=130,
            value=age_value,
            step=1,
            help="Enter the patient's age in years.",
        )
    )
    st.session_state.patient_gender = st.selectbox(
        "⚧ Gender",
        ["", "Male", "Female"],
        index=["", "Male", "Female"].index(st.session_state.patient_gender)
        if st.session_state.patient_gender in ["", "Male", "Female"]
        else 0,
    )

    st.markdown("---")
    st.checkbox(
        "I have read and agree to the medical disclaimer",
        value=st.session_state.agree_disclaimer,
        key="agree_disclaimer",
    )

    with st.expander("Saved profiles", expanded=False):
        if st.session_state.saved_profiles:
            saved_labels = [f"{p['name']} · {p['age']} · {p['gender']}" for p in st.session_state.saved_profiles]
            st.selectbox("Select a saved profile to load", [""] + saved_labels, key="selected_saved_profile")
            st.button("Load saved profile", key="load_saved_profile", on_click=load_saved_profile)
        else:
            st.info("No saved profiles yet. Save the current profile after completing the form.")

    profile_save_ready = bool(
        st.session_state.patient_name.strip()
        and st.session_state.patient_age.strip()
        and st.session_state.patient_gender != ""
    )

    valid_profile = bool(
        profile_save_ready
        and st.session_state.agree_disclaimer
    )

    if not valid_profile:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #eab308 0%, #dc2626 100%); 
                        color: #e8f3fc; 
                        padding: 1rem; 
                        border-radius: 12px; 
                        text-align: center; 
                        font-weight: 600; 
                        margin: 1.2rem 0;">
                ⚠️ Complete the patient profile and disclaimer to continue.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if profile_save_ready:
            st.info("You can still save this profile once the name, age, and gender are filled in.")
        st.button("Reset profile", key="reset_profile", on_click=reset_profile)
        st.markdown('</div>', unsafe_allow_html=True)
        render_custom_footer()
        st.stop()

    # Replaced st.columns with responsive flex layout for buttons
    st.markdown('<div class="responsive-button-grid">', unsafe_allow_html=True)
    st.button(
        "Begin Assessment",
        key="continue_to_analysis",
        on_click=continue_to_analysis,
        disabled=not valid_profile,
    )
    st.button(
        "Save profile",
        key="save_profile",
        on_click=save_profile,
        disabled=not profile_save_ready,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.profile_saved:
        st.success("Profile saved successfully. You can load it later from Saved profiles.")

    st.button("Reset profile", key="reset_profile", on_click=reset_profile)
    st.markdown('</div>', unsafe_allow_html=True)
    render_custom_footer()
    st.stop()


def render_analysis_chat_styles():
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark light;
        }
        .analysis-tool-shell {
            display: grid;
            gap: 1.25rem;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0.25rem;
        }
        .analysis-panel,
        .dashboard-shell,
        .assistant-panel,
        .analysis-report-box,
        .glass-card,
        .panel-card {
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(12, 24, 39, 0.85);
            box-shadow: 0 12px 28px rgba(0,0,0,0.22);
            padding: 1rem;
            color: inherit;
        }
        .analysis-heading {
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0 0 0.5rem;
            color: inherit;
        }
        .analysis-subheading {
            margin-bottom: 1rem;
            color: rgba(255,255,255,0.8);
            font-size: 0.95rem;
        }
        .analysis-action-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            align-items: stretch;
            margin-top: 1rem;
            padding: 0.8rem;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 14px;
        }
        .action-copy {
            flex: 1 1 100%;
            min-width: 200px;
            color: rgba(238, 244, 255, 0.85);
            font-size: 0.9rem;
        }
        .section-card {
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(6, 14, 26, 0.88);
            padding: 1.05rem;
            margin-bottom: 0.95rem;
        }
        .analysis-action-buttons {
            display: flex;
            gap: 0.6rem;
            flex-wrap: wrap;
            margin-top: 0.75rem;
        }
        .analysis-action-buttons .stButton>button,
        .analysis-action-buttons .stButton>div>button,
        .analysis-action-buttons .stButton>div>div>button {
            min-width: 140px !important;
            width: auto !important;
            padding: 0.72rem 1rem !important;
            border-radius: 12px !important;
            font-size: 0.91rem !important;
        }
        .tool-grid-wrap {
            display: grid;
            gap: 1rem;
        }
        .stColumns {
            display: grid !important;
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
        }
        .result-line {
            word-break: break-word;
            white-space: pre-wrap;
            font-size: 0.95rem;
        }
        @media (min-width: 980px) {
            .stColumns {
                grid-template-columns: repeat(12, minmax(0, 1fr)) !important;
            }
            .col-left, .col-right {
                width: 100%;
            }
            .col-left { grid-column: span 8; }
            .col-right { grid-column: span 4; }
            .analysis-tool-shell {
                width: 98%;
            }
        }
        .assistant-experience-section {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 100%;
            margin: 1.5rem 0 1.5rem;
            padding: 1.8rem 1.5rem;
            border-radius: 22px;
            background: rgba(10, 18, 34, 0.84);
            border: 1px solid rgba(94, 202, 255, 0.15);
            box-shadow: 0 24px 80px rgba(4, 18, 38, 0.28);
            backdrop-filter: blur(18px);
            overflow: hidden;
            box-sizing: border-box;
        }
        .assistant-experience-section::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 10% 10%, rgba(45, 207, 255, 0.12), transparent 20%),
                        radial-gradient(circle at 85% 20%, rgba(142, 96, 255, 0.10), transparent 18%),
                        radial-gradient(circle at 50% 90%, rgba(89, 183, 255, 0.08), transparent 22%);
            pointer-events: none;
            filter: blur(10px);
            opacity: 0.9;
        }
        .assistant-experience-section::after {
            content: '';
            position: absolute;
            inset: 0;
            background-image: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.00) 100%);
            opacity: 0.18;
            pointer-events: none;
        }
        .input-section, .action-section, .output-section, .assistant-section {
            border-radius: 16px;
            border: 1px solid rgba(221, 234, 255, 0.15);
            background: rgba(9, 14, 28, 0.82);
            box-shadow: 0 12px 26px rgba(2, 6, 14, 0.25);
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .input-section .glass-card {
            margin-bottom: 1rem;
        }
        .action-section {
            background: rgba(17, 28, 50, 0.9);
        }
        .output-section {
            background: rgba(6, 12, 22, 0.86);
        }
        .assistant-section {
            background: rgba(10, 18, 34, 0.84);
            border: 1px solid rgba(94, 202, 255, 0.15);
            box-shadow: 0 24px 80px rgba(4, 18, 38, 0.28);
        }
        .assistant-panel {
            position: sticky;
            top: 1rem;
            z-index: 1;
        }
        .assistant-panel .assistant-title {
            font-size: 1.17rem;
            font-weight: 800;
            margin-bottom: 0.6rem;
            color: #e7f4ff;
        }
        .assistant-panel .assistant-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 0.8rem;
        }
        .assistant-panel .assistant-chip {
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            background: rgba(34, 155, 255, 0.18);
            color: #d7f3ff;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .assistant-panel .assistant-card {
            margin-bottom: 0.85rem;
            padding: 0.85rem;
            border-radius: 16px;
            background: rgba(17, 28, 50, 0.95);
            border: 1px solid rgba(88, 170, 255, 0.17);
        }
        .analysis-report-box {
            border-radius: 16px;
            border: 1px solid rgba(180, 225, 255, 0.16);
            background: rgba(6, 12, 22, 0.86);
        }
        .upload-report-hover {
            position: relative;
            display: inline-block;
            cursor: help;
            color: #c6dcff;
        }
        .upload-report-hover .upload-report-card {
            display: none;
            position: absolute;
            top: 120%;
            left: 0;
            width: 360px;
            padding: 0.7rem;
            border: 1px solid rgba(180, 225, 255, 0.24);
            background: rgba(8, 17, 33, 0.96);
            border-radius: 12px;
            box-shadow: 0 14px 30px rgba(0, 0, 0, 0.35);
            z-index: 10;
        }
        .upload-report-hover:hover .upload-report-card {
            display: block;
        }
        @media (max-width: 980px) {
            .stColumns {
                grid-template-columns: 1fr !important;
            }
            .analysis-action-bar {
                flex-direction: column;
                align-items: stretch;
            }
            .assistant-panel {
                position: static;
                top: auto;
            }
        }
        @media (max-width: 680px) {
            .analysis-tool-shell {
                padding: 0.25rem;
            }
            .analysis-action-bar {
                gap: 0.5rem;
            }
            .assistant-panel .assistant-chip-row {
                justify-content: flex-start;
            }
            .assistant-panel .assistant-card {
                padding: 0.7rem;
            }
            .input-section, .action-section, .output-section, .assistant-section {
                padding: 0.75rem;
            }
        }
        """,
        unsafe_allow_html=True,
    )


def render_chat_styles():
    st.markdown(
        """
        <style>
        .chat-shell {
            width: 100%;
            max-width: 980px;
            margin: 0 auto 1.5rem;
            background: #07101d;
            border-radius: 28px;
            box-shadow: 0 26px 60px rgba(0,0,0,0.18);
            overflow: hidden;
            position: relative;
            z-index: 1;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .chat-shell header {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            justify-content: space-between;
            background: linear-gradient(135deg, #075e54 0%, #128c7e 100%);
            padding: 1rem 1.25rem;
            color: #ffffff;
        }
        .chat-shell .avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: rgba(255,255,255,0.12);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: 800;
            border: 1px solid rgba(255,255,255,0.16);
        }
        .chat-shell .chat-title {
            margin: 0;
            font-size: 1.2rem;
            font-weight: 800;
        }
        .chat-shell .chat-subtitle {
            margin: 0.25rem 0 0;
            font-size: 0.92rem;
            color: rgba(255,255,255,0.9);
        }
        .chat-window {
            background: #0f1f30;
            padding: 1rem 1rem 0;
            min-height: 0;
            max-height: 62vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 0.85rem;
        }
        .chat-window::-webkit-scrollbar {
            width: 10px;
        }
        .chat-window::-webkit-scrollbar-thumb {
            background: rgba(0,0,0,0.18);
            border-radius: 999px;
        }
        .bubble {
            display: inline-flex;
            flex-direction: column;
            max-width: 78%;
            padding: 0.95rem 1rem;
            border-radius: 18px;
            line-height: 1.6;
            word-break: break-word;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }
        .bubble.user {
            background: #25d366;
            color: #0b1721;
            align-self: flex-end;
            margin-left: auto;
            border-bottom-right-radius: 4px;
            border-top-left-radius: 18px;
        }
        .bubble.assistant {
            background: #1a293c;
            color: #e8eff7;
            align-self: flex-start;
            margin-right: auto;
            border-bottom-left-radius: 4px;
            border-top-right-radius: 18px;
        }
        .bubble.assistant.alt {
            background: #1b2b43;
            color: #d5e3ff;
        }
        .chat-input-panel {
            background: #0e1b2d;
            padding: 1rem 1rem 1.1rem;
            border-top: 1px solid rgba(255,255,255,0.08);
            display: grid;
            gap: 0.75rem;
        }
        .chat-shell .stButton>button,
        .chat-shell .stButton>div>button,
        .chat-shell .stButton>div>div>button {
            background: rgba(255,255,255,0.08) !important;
            color: #e8eff7 !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            border-radius: 18px !important;
            min-height: 3.4rem !important;
            box-shadow: none !important;
        }
        .chat-shell .stButton>button:hover,
        .chat-shell .stButton>div>button:hover,
        .chat-shell .stButton>div>div>button:hover {
            background: rgba(255,255,255,0.14) !important;
        }
        .chat-input-panel .stButton>button,
        .chat-input-panel .stButton>div>button,
        .chat-input-panel .stButton>div>div>button {
            min-height: 3.6rem !important;
        }
        .chat-input-panel .stButton>button:hover,
        .chat-input-panel .stButton>div>button:hover,
        .chat-input-panel .stButton>div>div>button:hover {
            background: rgba(255,255,255,0.14) !important;
        }
        .chat-prompt-panel {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            padding: 1rem 0 0;
        }
        .chat-prompt-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.65rem 0.95rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            color: #e8eff7;
            font-size: 0.92rem;
        }
        .chat-input-panel input[type="text"] {
            width: 100% !important;
            height: 4rem !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            padding: 1rem !important;
            color: #e8eff7 !important;
            background: #0b1726 !important;
            box-shadow: none !important;
        }
        .chat-close-row {
            display: flex;
            justify-content: flex-end;
            padding: 0.8rem 1rem 0;
        }
        @media (max-width: 980px) {
            .chat-shell {
                max-width: 100%;
            }
            .chat-window {
                padding: 1rem 0.85rem 0;
            }
        }
        @media (max-width: 640px) {
            .chat-shell header {
                flex-direction: column;
                align-items: flex-start;
            }
            .chat-input-row {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def fill_chat_prompt(suggestion, input_key):
    st.session_state[input_key] = suggestion
    st.session_state.chat_warning = ""
    st.session_state.chat_error = ""


def clear_chat_history(mode=None):
    if mode == "medical":
        st.session_state.chat_history_medical = []
    else:
        st.session_state.chat_history_quick = []
    st.session_state.chat_warning = ""
    st.session_state.chat_error = ""
    st.rerun()


def handle_chat_submit(input_key, mode):
    if not st.session_state.get(input_key, "").strip():
        st.session_state.chat_warning = "Please enter a question before sending."
        st.session_state.chat_error = ""
        return

    user_prompt = st.session_state[input_key].strip()
    prompt_text = user_prompt
    patient_context_parts = []
    if st.session_state.get("patient_name"):
        patient_context_parts.append(f"Patient name: {st.session_state.patient_name}.")
    if st.session_state.get("patient_age"):
        patient_context_parts.append(f"Patient age: {st.session_state.patient_age}.")
    if st.session_state.get("patient_gender"):
        patient_context_parts.append(f"Patient gender: {st.session_state.patient_gender}.")
    if st.session_state.get("uploaded_images"):
        file_names = ", ".join([img.name for img in st.session_state.uploaded_images])
        patient_context_parts.append(f"Uploaded clinical image files: {file_names}.")

    if patient_context_parts:
        prompt_text = " ".join(patient_context_parts) + " Question: " + prompt_text

    last_submit = st.session_state.get("last_chat_submit", {"prompt": "", "mode": "", "time": 0.0})
    if (
        last_submit["prompt"] == prompt_text
        and last_submit["mode"] == mode
        and time.time() - last_submit["time"] < 1.0
    ):
        return
    st.session_state.last_chat_submit = {
        "prompt": prompt_text,
        "mode": mode,
        "time": time.time(),
    }
    try:
        with st.spinner("Generating response from Nirnay..."):
            if "GROQ_API_KEY" in st.secrets:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            else:
                client = Groq()

            system_prompt = (
            "You are a medical assistant. Provide general medical information only, not medical advice. Answer in clear, complete points and full sentences. Avoid using tables. Prefer numbered or bulleted lists when summarizing symptoms, causes, or steps. Do not truncate the reply; complete the answer fully. Always remind users to consult a qualified healthcare provider for final clinical decisions. Respond in the same language as the user's query. Support all international languages, including Indian languages such as Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and others."
            if mode == "medical"
            else "You are a medical assistant. Answer briefly and compactly in 1-2 short sentences. Provide general medical information only, not medical advice. Always remind users to consult a qualified healthcare provider for final clinical decisions. Respond in the same language as the user's query. Support all international languages, including Indian languages such as Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and others."
        )

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_text},
            ],
            max_completion_tokens=2048 if mode == "medical" else 420,
            temperature=0.4,
            stream=False,
        )

        bot_response = ""
        if hasattr(completion.choices[0].message, "content"):
            bot_response = completion.choices[0].message.content
        elif isinstance(completion.choices[0].message, dict):
            bot_response = completion.choices[0].message.get("content", "")
        elif hasattr(completion.choices[0], "text"):
            bot_response = completion.choices[0].text

        bot_response = bot_response or "No response received from the AI."
        st.session_state.chat_last_user = user_prompt
        st.session_state.chat_last_response = bot_response
        history_key = "chat_history_medical" if mode == "medical" else "chat_history_quick"
        if history_key not in st.session_state:
            st.session_state[history_key] = []
        st.session_state[history_key].append({"role": "user", "content": user_prompt})
        st.session_state[history_key].append({"role": "assistant", "content": bot_response})
        st.session_state[input_key] = ""
        st.session_state.chat_error = ""
        st.session_state.chat_warning = ""
    except Exception as exc:
        st.session_state.chat_error = f"AI chatbot error: {exc}"
        st.session_state.chat_warning = ""

# ------------ Helpers -------------
def parse_float(val):
    if val is None or str(val).strip() == "":
        return None
    try:
        return float(val)
    except ValueError:
        return None


def infer_image_context(filename):
    lower_name = filename.lower()
    if any(term in lower_name for term in ["wound", "ulcer", "lesion", "skin", "derm", "dermatology"]):
        return "Wound / dermatology image"
    if any(term in lower_name for term in ["xray", "x-ray", "chest", "radiograph", "radiography"]):
        return "X-ray image"
    if any(term in lower_name for term in ["ct", "ctscan", "ct-scan", "computed tomography"]):
        return "CT scan image"
    if any(term in lower_name for term in ["mri", "magnetic resonance", "mr"]):
        return "MRI image"
    if any(term in lower_name for term in ["ultrasound", "us", "sonogram"]):
        return "Ultrasound image"
    return "Clinical image"


def generate_uploaded_image_insights(uploaded_images, patient_name, patient_age, patient_gender):
    if not uploaded_images:
        return []

    files_description = "\n".join(
        [f"- {img.type or 'unknown'} image, {img.size // 1024} KB" for img in uploaded_images]
    )
    prompt = (
        f"Patient: {patient_name or 'Unknown'}, Age: {patient_age or 'N/A'}, Gender: {patient_gender or 'N/A'}. "
        f"{len(uploaded_images)} clinical image file(s) were uploaded with the following metadata:\n{files_description}\n\n"
        "Suggest the most likely imaging context and possible findings to review without asking any clinical questions. "
        "Do not infer any diagnosis or finding from the filename or filename-like labels. "
        "Do not include any prefix about metadata, file size, or image source. "
        "Present the response as a single concise paragraph."
    )

    try:
        with st.spinner("Analyzing uploaded files with AI..."):
            response = run_groq_chat_sync(prompt)
        if response:
            paragraph = " ".join([line.strip() for line in response.splitlines() if line.strip()])
            paragraph = re.sub(
                r"^Based (?:solely )?on(?: the)? (?:limited )?metadata\s*\([^\)]*\),\s*", "", paragraph,
                flags=re.IGNORECASE,
            )
            paragraph = re.sub(
                r"^Based (?:solely )?on(?: the)? metadata,\s*", "", paragraph,
                flags=re.IGNORECASE,
            )
            paragraph = re.sub(
                r"^Based (?:solely )?on(?: the)? (?:limited )?metadata\s*[\.:]?\s*", "", paragraph,
                flags=re.IGNORECASE,
            )
            return paragraph
        return "Image insight generation returned empty. Using metadata-only context."
    except Exception as exc:
        return f"Image insight generation failed: {exc}. Using metadata-only context."


def summarize_uploaded_files(uploaded_images, patient_name, patient_age, patient_gender):
    summary = ["\n=== 📷 UPLOADED IMAGE REVIEW ==="]
    for img in uploaded_images:
        context = infer_image_context(img.name)
        summary.append(
            f"[INFO] {context} attached ({img.type or 'unknown'}, {img.size // 1024} KB)."
        )

    ai_text = generate_uploaded_image_insights(uploaded_images, patient_name, patient_age, patient_gender)
    st.session_state.uploaded_image_report = ai_text
    if ai_text:
        summary.append(f"[INFO] {ai_text}")

    summary.append("[INFO] Review the attached files for visual findings and compare them with the clinical data entered.")
    return summary


def suggest_analysis_followup_questions(collected):
    question_map = [
        (
            "🧪 Metabolism",
            collected.get("metabolism", {}),
            "Add glucose metrics, lipid markers, or classic diabetes symptoms such as thirst, polyuria, or slow wound healing.",
        ),
        (
            "❤️ Cardiac",
            collected.get("cardiac", {}),
            "Add blood pressure, troponin, BNP, or chest pain/shortness of breath symptoms.",
        ),
        (
            "🧬 Oncology",
            collected.get("oncology", {}),
            "Add mass size, weight loss, lymph node changes, tumor marker values, or new systemic symptoms.",
        ),
        (
            "🧠 Neurology",
            collected.get("neurology", {}),
            "Add headaches, weakness, sensory changes, seizures, dizziness, or focal deficit details.",
        ),
        (
            "👩 Gynecology",
            collected.get("gynecology", {}),
            "Add menstrual changes, pelvic pain, discharge, infertility symptoms, or gynecologic exam findings.",
        ),
        (
            "🛡️ Immunology",
            collected.get("immunology", {}),
            "Add autoimmune markers, recurrent infection history, rashes, joint pain, or lymph node findings.",
        ),
        (
            "🦋 Endocrinology",
            collected.get("endocrinology", {}),
            "Add thyroid labs, cortisol/PTH levels, metabolic symptoms, or hormone-related complaints.",
        ),
        (
            "👶 Pediatric",
            collected.get("pediatric", {}),
            "Add growth measures, developmental milestones, feeding issues, fever, or respiratory symptoms.",
        ),
        (
            "🧴 Dermatology",
            collected.get("dermatology", {}),
            "Add rash description, lesion size, itching, scaling, or ulcer characteristics.",
        ),
        (
            "🧠 Psychiatry",
            collected.get("psychiatry", {}),
            "Add mood, anxiety, sleep, cognitive impairment, or suicide risk details.",
        ),
        (
            "💧 Nephrology",
            collected.get("nephrology", {}),
            "Add kidney labs, urine changes, edema, blood in urine, or fluid balance concerns.",
        ),
        (
            "🩸 Hematology",
            collected.get("hematology", {}),
            "Add hemoglobin, platelet or white count values, bleeding, bruising, or lymphadenopathy symptoms.",
        ),
    ]
    followups = []
    for label, section, prompt in question_map:
        if not has_data(section.values()):
            followups.append(f"{label}: {prompt}")
    if not followups:
        followups.append("If you want a more precise report, add more measurements or symptoms in the relevant tabs and upload any available imaging.")
    return followups


def chunked(values, size):
    for i in range(0, len(values), size):
        yield values[i : i + size]


def has_data(values):
    return any(v is True for v in values if isinstance(v, bool)) or any(
        v is not None for v in values if not isinstance(v, bool)
    )


def make_inputs(tab, fields):
    out = {}
    numbers = [(k, v) for k, v in fields.items() if v["type"] == "num"]
    checks = [(k, v) for k, v in fields.items() if v["type"] == "chk"]

    # Use three columns for input fields so labels stay visible in both PC and smartphone layouts.
    if numbers:
        for row in chunked(numbers, 3):
            cols = tab.columns(len(row))
            for col, (k, v) in zip(cols, row):
                out[k] = parse_float(col.text_input(v["label"], key=f"{v['id']}"))

    # Use three columns for checkboxes to keep the form compact and labels readable.
    if checks:
        # Collapse symptom checkboxes by default so the UI stays clean.
        expander = tab.expander("Symptoms & clinical signs", expanded=True)
        with expander:
            for row in chunked(checks, 3):
                cols = expander.columns(len(row))
                for col, (k, v) in zip(cols, row):
                    out[k] = col.checkbox(v["label"], key=f"{v['id']}")

    return out


def val(entry_key, dict_obj):
    if entry_key in dict_obj:
        return dict_obj[entry_key]
    return None


def put_message(txt):
    st.write(txt)


def run_groq_chat(prompt, model="openai/gpt-oss-120b"):
    client = Groq()
    messages = [
        {
            "role": "system",
            "content": (
                "You are Nirnay, a professional medical diagnostic assistant. "
                "Provide concise, clinically responsible guidance and remind users to consult a qualified healthcare provider."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        delta = ""
        try:
            delta = chunk.choices[0].delta.content or ""
        except Exception:
            try:
                delta = chunk.choices[0].delta.get("content", "") or ""
            except Exception:
                delta = ""
        response += delta
        yield response


def run_groq_chat_sync(prompt, model="openai/gpt-oss-120b"):
    client = Groq()
    messages = [
        {
            "role": "system",
            "content": (
                "You are Nirnay, a professional medical diagnostic assistant. "
                "Provide concise, clinically responsible guidance and remind users to consult a qualified healthcare provider. "
                "Respond in the same language as the user's query. Support all international languages, including Indian languages such as Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and others."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=2048,
        top_p=1,
        stream=False,
    )

    if hasattr(completion.choices[0].message, "content"):
        return completion.choices[0].message.content or ""
    if isinstance(completion.choices[0].message, dict):
        return completion.choices[0].message.get("content", "") or ""
    return getattr(completion.choices[0], "text", "") or ""

if page == "chat":
    render_navbar()
    mode = st.session_state.get("chat_mode", "medical")
    header = "Nirnay Clinical Advisor" if mode == "medical" else "Nirnay Rapid Triage"
    subtitle = (
        "Ask Nirnay a clinical question about this patient in any language and receive a full assessment response."
        if mode == "medical"
        else "Ask a short clinical question in any language and receive a focused triage recommendation."
    )
    prompt_label = (
        "Type your clinical question in any language..."
        if mode == "medical"
        else "Type your quick triage question in any language..."
    )
    send_label = "Ask Advisor" if mode == "medical" else "Ask Triage"
    form_key = "nirnay_chat_form" if mode == "medical" else "nirnay_chat_alt_form"
    input_key = "nirnay_chat_prompt" if mode == "medical" else "nirnay_chat_prompt_alt"

    render_chat_styles()

    if "chat_last_user" not in st.session_state:
        st.session_state.chat_last_user = ""
    if "chat_last_response" not in st.session_state:
        st.session_state.chat_last_response = ""
    if "chat_error" not in st.session_state:
        st.session_state.chat_error = ""
    if "chat_warning" not in st.session_state:
        st.session_state.chat_warning = ""

    st.markdown("<div class='chat-shell'>", unsafe_allow_html=True)
    # Replaced st.columns with responsive flex layout for action buttons
    st.markdown('<div class="responsive-action-grid">', unsafe_allow_html=True)
    st.button(
        "🗑️ Clear Conversation",
        key=f"clear_chat_{mode}_button",
        on_click=clear_chat_history,
        args=(mode,),
    )
    st.button(
        "⬅️ Back to Analysis",
        key=f"back_{mode}_button",
        on_click=back_to_analysis,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"<header><div class='avatar'>{'👩‍⚕️' if mode == 'medical' else '⚡'}</div><div><div class='chat-title'>{header}</div><div class='chat-subtitle'>{subtitle}</div></div></header>",
        unsafe_allow_html=True,
    )

    # Replaced st.columns with responsive flex layout for chat mode switches
    st.markdown('<div class="responsive-chat-mode-grid">', unsafe_allow_html=True)
    st.button(
        "Medical Assistant",
        key="chat_mode_med_button",
        disabled=mode == "medical",
        on_click=launch_chat,
        args=("medical",),
    )
    st.button(
        "Quick Assistant",
        key="chat_mode_quick_button",
        disabled=mode == "quick",
        on_click=launch_chat,
        args=("quick",),
    )
    st.markdown('</div>', unsafe_allow_html=True)

    context_items = []
    if st.session_state.get("patient_name"):
        context_items.append(f"Patient: {st.session_state.patient_name}")
    if st.session_state.get("patient_age"):
        context_items.append(f"Age: {st.session_state.patient_age}")
    if st.session_state.get("patient_gender"):
        context_items.append(f"Gender: {st.session_state.patient_gender}")
    if st.session_state.get("uploaded_images"):
        context_items.append(f"Uploaded files: {len(st.session_state.uploaded_images)}")
    if context_items:
        st.markdown(
            f"<div class='hint-box'><strong>Session context:</strong> {html.escape(' · '.join(context_items))}</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='chat-prompt-panel'>"
        + "<span class='chat-prompt-chip'>What are the key red flags for this symptom?</span>"
        + "<span class='chat-prompt-chip'>How should I interpret these lab values?</span>"
        + "<span class='chat-prompt-chip'>List the top 3 differential diagnoses.</span>"
        + "<span class='chat-prompt-chip'>What next test is most useful?</span>"
        + "</div>",
        unsafe_allow_html=True,
    )

    suggestion_texts = [
        "What are the most urgent concerns for this patient?",
        "Which findings need immediate follow-up?",
        "What additional tests are recommended next?",
    ] if mode == "medical" else [
        "Summarize the main concern in one sentence.",
        "Give a quick next step for this presentation.",
        "What is the likely diagnosis?",
    ]
    # Replaced st.columns with responsive flex layout for suggestion buttons
    st.markdown('<div class="responsive-suggestion-grid">', unsafe_allow_html=True)
    for idx, suggestion in enumerate(suggestion_texts):
        st.button(
            suggestion,
            key=f"chat_suggestion_{mode}_{idx}",
            on_click=fill_chat_prompt,
            args=(suggestion, input_key),
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div class='chat-window'>", unsafe_allow_html=True)

    history_key = "chat_history_medical" if mode == "medical" else "chat_history_quick"
    history = st.session_state.get(history_key, [])

    if history:
        for msg in history:
            content_html = html.escape(msg["content"]).replace("\n", "<br>")
            if msg["role"] == "user":
                bubble_class = "bubble user"
            else:
                bubble_class = "bubble assistant" if mode == "medical" else "bubble assistant alt"
            st.markdown(
                f"<div class='{bubble_class}'>{content_html}</div>",
                unsafe_allow_html=True,
            )
    else:
        welcome_text = (
            "Hello! I'm Nirnay. Ask me any clinical question in any language to begin." if mode == "medical" else "Hello! I'm Quick Nirnay. Ask me a short clinical question in any language for a compact answer."
        )
        st.markdown(
            f"<div class='bubble assistant'>{html.escape(welcome_text)}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <script>
        const chatWindow = document.querySelector('.chat-window');
        if (chatWindow) {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
        window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
        </script>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.chat_error:
        st.error(st.session_state.chat_error)
    if st.session_state.chat_warning:
        st.warning(st.session_state.chat_warning)

    st.markdown("<div class='chat-input-panel'>", unsafe_allow_html=True)
    user_input = st.text_input(prompt_label, key=input_key, placeholder=prompt_label, label_visibility='collapsed')
    st.button(send_label, key=f"{form_key}_submit", on_click=handle_chat_submit, args=(input_key, mode))
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    render_custom_footer()
    st.stop()

# ------------ Field definitions (copying your categories) -------------
vital_defs = {
    "f_glc": {"type": "num", "label": "Fasting Glucose (mmol/L)", "id":"v_f_glc"},
    "a1c": {"type": "num", "label": "HbA1c (%)", "id":"v_a1c"},
    "ins": {"type": "num", "label": "Fasting Insulin (µIU/mL)", "id":"v_ins"},
    "uric": {"type": "num", "label": "Uric Acid (mg/dL)", "id":"v_uric"},
    "tsh": {"type": "num", "label": "TSH (mIU/L)", "id":"v_tsh"},
    "t3": {"type": "num", "label": "Free T3 (pg/mL)", "id":"v_t3"},
    "t4": {"type": "num", "label": "Free T4 (ng/dL)", "id":"v_t4"},
    "crea": {"type": "num", "label": "Creatinine (mg/dL)", "id":"v_crea"},
    "egfr": {"type": "num", "label": "eGFR (mL/min/1.73 m²)", "id":"v_egfr"},
    "alt": {"type": "num", "label": "ALT (U/L)", "id":"v_alt"},
    "ast": {"type": "num", "label": "AST (U/L)", "id":"v_ast"},
    "ggt": {"type": "num", "label": "GGT (U/L)", "id":"v_ggt"},
    "bmi": {"type": "num", "label": "BMI (kg/m²)", "id":"v_bmi"},
    "temp": {"type": "num", "label": "Basal Temp (°C)", "id":"v_temp"},
    "poly": {"type": "chk", "label": "Polydipsia (Thirst)", "id":"v_poly"},
    "urin": {"type": "chk", "label": "Polyuria (Urination)", "id":"v_urin"},
    "acan": {"type": "chk", "label": "Acanthosis Nigricans", "id":"v_acan"},
    "fatg": {"type": "chk", "label": "Post-Prandial Fatigue", "id":"v_fatg"},
    "crave": {"type": "chk", "label": "Sugar Cravings", "id":"v_crave"},
    "heal": {"type": "chk", "label": "Slow Wound Healing", "id":"v_heal"},
    "blur": {"type": "chk", "label": "Blurred Vision", "id":"v_blur"},
    "oed": {"type": "chk", "label": "Ankle Oedema", "id":"v_oed"},
    "breath": {"type": "chk", "label": "Acetone Breath", "id":"v_breath"},
    "ting": {"type": "chk", "label": "Peripheral Tingling", "id":"v_ting"},
    "hair": {"type": "chk", "label": "Brittle Hair/Nails", "id":"v_hair"},
}

cardiac_defs = {
    "trop": {"type": "num", "label": "Troponin-I (ng/L)", "id":"c_trop"},
    "bnp": {"type": "num", "label": "BNP Marker (pg/mL)", "id":"c_bnp"},
    "hscrp": {"type": "num", "label": "hs-CRP (mg/L)", "id":"c_hscrp"},
    "ldl": {"type": "num", "label": "LDL Cholesterol (mg/dL)", "id":"c_ldl"},
    "hdl": {"type": "num", "label": "HDL Cholesterol (mg/dL)", "id":"c_hdl"},
    "trig": {"type": "num", "label": "Triglycerides (mg/dL)", "id":"c_trig"},
    "sys": {"type": "num", "label": "Systolic BP (mmHg)", "id":"c_sys"},
    "dia": {"type": "num", "label": "Diastolic BP (mmHg)", "id":"c_dia"},
    "hr": {"type": "num", "label": "Resting HR (bpm)", "id":"c_hr"},
    "lpa": {"type": "num", "label": "Lipoprotein(a) (mg/dL)", "id":"c_lpa"},
    "angina": {"type": "chk", "label": "Chest Pressure", "id":"c_angina"},
    "ortho": {"type": "chk", "label": "Orthopnea", "id":"c_ortho"},
    "pnd": {"type": "chk", "label": "Paroxysmal Dyspnea", "id":"c_pnd"},
    "edema": {"type": "chk", "label": "Pitting Edema", "id":"c_edema"},
    "palp": {"type": "chk", "label": "Palpitations", "id":"c_palp"},
    "sync": {"type": "chk", "label": "Syncope (Fainting)", "id":"c_sync"},
    "cyan": {"type": "chk", "label": "Peripheral Cyanosis", "id":"c_cyan"},
    "jvp": {"type": "chk", "label": "Raised JVP", "id":"c_jvp"},
    "club": {"type": "chk", "label": "Digital Clubbing", "id":"c_club"},
    "claud": {"type": "chk", "label": "Leg Claudication", "id":"c_claud"},
    "cold": {"type": "chk", "label": "Cold Extremities", "id":"c_cold"},
    "murm": {"type": "chk", "label": "Audible Murmur", "id":"c_murm"},
    "cough": {"type": "chk", "label": "Frothy Cough", "id":"c_cough"},
    "sweat": {"type": "chk", "label": "Cold Sweats", "id":"c_sweat"},
    "nausea": {"type": "chk", "label": "Unexplained Nausea", "id":"c_nausea"},
}

onco_defs = {
    "psa": {"type": "num", "label": "PSA (ng/mL)", "id":"o_psa"},
    "ca125": {"type": "num", "label": "CA-125 (U/mL)", "id":"o_ca125"},
    "cea": {"type": "num", "label": "CEA (ng/mL)", "id":"o_cea"},
    "afp": {"type": "num", "label": "AFP (ng/mL)", "id":"o_afp"},
    "ca19": {"type": "num", "label": "CA 19-9 (U/mL)", "id":"o_ca19"},
    "ldh": {"type": "num", "label": "LDH (U/L)", "id":"o_ldh"},
    "size": {"type": "num", "label": "Mass Diameter (cm)", "id":"o_size"},
    "weight": {"type": "num", "label": "Unintended Weight Loss (kg)", "id":"o_weight"},
    "mass": {"type": "chk", "label": "Non-Mobile Mass", "id":"o_mass"},
    "node": {"type": "chk", "label": "Lymphadenopathy", "id":"o_node"},
    "meta": {"type": "chk", "label": "Bone/Lung Pain", "id":"o_meta"},
    "night": {"type": "chk", "label": "Night Sweats", "id":"o_night"},
    "hemopt": {"type": "chk", "label": "Hemoptysis (Cough Blood)", "id":"o_hemopt"},
    "dysph": {"type": "chk", "label": "Dysphagia", "id":"o_dysph"},
    "change": {"type": "chk", "label": "Bowel Habit Change", "id":"o_change"},
    "mole": {"type": "chk", "label": "Evolving Mole", "id":"o_mole"},
    "hema": {"type": "chk", "label": "Hematuria (Blood in Urine)", "id":"o_hema"},
    "ascit": {"type": "chk", "label": "Abdominal Ascites", "id":"o_ascit"},
    "jaund": {"type": "chk", "label": "Icterus/Jaundice", "id":"o_jaund"},
    "fract": {"type": "chk", "label": "Pathological Fracture", "id":"o_fract"},
    "cachex": {"type": "chk", "label": "Muscle Wasting", "id":"o_cachex"},
    "pleur": {"type": "chk", "label": "Pleuritic Pain", "id":"o_pleur"},
    "anem": {"type": "chk", "label": "Refractory Anemia", "id":"o_anem"},
    "fev": {"type": "chk", "label": "FUO (Fever Unknown Origin)", "id":"o_fev"},
    "itch": {"type": "chk", "label": "Pruritus (Severe Itch)", "id":"o_itch"},
}

neural_defs = {
    "tonic": {"type": "chk", "label": "Grand Mal (Convulsions)", "id":"n_tonic"},
    "stare": {"type": "chk", "label": "Absence Spells", "id":"n_stare"},
    "myo": {"type": "chk", "label": "Myoclonic Jerks", "id":"n_myo"},
    "aura": {"type": "chk", "label": "Visual/Smell Aura", "id":"n_aura"},
    "post": {"type": "chk", "label": "Post-Ictal Amnesia", "id":"n_post"},
    "atax": {"type": "chk", "label": "Gait Ataxia", "id":"n_atax"},
    "trem": {"type": "chk", "label": "Resting Tremor", "id":"n_trem"},
    "rigi": {"type": "chk", "label": "Cogwheel Rigidity", "id":"n_rigi"},
    "ptos": {"type": "chk", "label": "Ptosis (Droopy Eyelid)", "id":"n_ptos"},
    "slur": {"type": "chk", "label": "Dysarthria (Slurred)", "id":"n_slur"},
    "weak": {"type": "chk", "label": "Hemiparesis (Weakness)", "id":"n_weak"},
    "sens": {"type": "chk", "label": "Paresthesia (Numbness)", "id":"n_sens"},
    "phot": {"type": "chk", "label": "Photophobia", "id":"n_phot"},
    "vert": {"type": "chk", "label": "Vertigo/Dizziness", "id":"n_vert"},
    "memo": {"type": "chk", "label": "Memory Deficit", "id":"n_memo"},
    "migr": {"type": "chk", "label": "Chronic Migraine", "id":"n_migr"},
    "tinn": {"type": "chk", "label": "Tinnitus", "id":"n_tinn"},
    "dipl": {"type": "chk", "label": "Diplopia (Double Vision)", "id":"n_dipl"},
    "dysf": {"type": "chk", "label": "Aphasia (Speech Struggle)", "id":"n_dysf"},
    "cogn": {"type": "chk", "label": "Cognitive Fog", "id":"n_cogn"},
    "neur": {"type": "chk", "label": "Neuralgia (Sharp Pain)", "id":"n_neur"},
    "hic": {"type": "chk", "label": "Increased ICP signs", "id":"n_hic"},
    "radic": {"type": "chk", "label": "Radicular Pain", "id":"n_radic"},
    "babin": {"type": "chk", "label": "Babinski Sign", "id":"n_babin"},
    "pupil": {"type": "chk", "label": "Unequal Pupils", "id":"n_pupil"},
}

gynae_defs = {
    "pcos": {"type": "chk", "label": "PCOS Markers", "id":"g_pcos"},
    "endo": {"type": "chk", "label": "Endometriosis Pain", "id":"g_endo"},
    "lesi": {"type": "chk", "label": "Genital Ulcers", "id":"g_lesi"},
    "puru": {"type": "chk", "label": "Purulent Discharge", "id":"g_puru"},
    "pelv": {"type": "chk", "label": "Pelvic Inflammatory signs", "id":"g_pelv"},
    "amen": {"type": "chk", "label": "Amenorrhea", "id":"g_amen"},
    "dysme": {"type": "chk", "label": "Dysmenorrhea", "id":"g_dysme"},
    "hirs": {"type": "chk", "label": "Hirsutism", "id":"g_hirs"},
    "spot": {"type": "chk", "label": "Intermenstrual Spotting", "id":"g_spot"},
    "dyspa": {"type": "chk", "label": "Dyspareunia", "id":"g_dyspa"},
    "infert": {"type": "chk", "label": "Primary Infertility", "id":"g_infert"},
    "libi": {"type": "chk", "label": "Reduced Libido", "id":"g_libi"},
    "vagin": {"type": "chk", "label": "Vaginitis/Itching", "id":"g_vagin"},
    "balan": {"type": "chk", "label": "Balanitis", "id":"g_balan"},
    "ureth": {"type": "chk", "label": "Urethritis", "id":"g_ureth"},
    "lymph": {"type": "chk", "label": "Buboes/Inguinal Nodes", "id":"g_lymph"},
    "warta": {"type": "chk", "label": "Genital Warts", "id":"g_warta"},
    "chan": {"type": "chk", "label": "Painless Chancre", "id":"g_chan"},
    "cyst": {"type": "chk", "label": "Ovarian Cyst Signs", "id":"g_cyst"},
    "mast": {"type": "chk", "label": "Mastalgia", "id":"g_mast"},
    "bloat": {"type": "chk", "label": "Persistent Bloating", "id":"g_bloat"},
    "menop": {"type": "chk", "label": "Hot Flashes", "id":"g_menop"},
    "prola": {"type": "chk", "label": "Uterine Prolapse signs", "id":"g_prola"},
    "herp": {"type": "chk", "label": "Vesicular Herpes", "id":"g_herp"},
    "cand": {"type": "chk", "label": "Thick White Discharge", "id":"g_cand"},
    "rayn": {"type": "chk", "label": "Raynaud's Phenomenon", "id":"g_rayn"},
    "sicca": {"type": "chk", "label": "Dry Eyes/Mouth", "id":"g_sicca"},
}

immuno_defs = {
    "cd4": {"type": "num", "label": "CD4 Count (cells/µL)", "id":"i_cd4"},
    "ana": {"type": "num", "label": "ANA Titer (ratio)", "id":"i_ana"},
    "esr": {"type": "num", "label": "ESR (mm/hr)", "id":"i_esr"},
    "wbc": {"type": "num", "label": "WBC Count (×10³/µL)", "id":"i_wbc"},
    "igg": {"type": "num", "label": "IgG Levels (mg/dL)", "id":"i_igg"},
    "crp": {"type": "num", "label": "CRP Levels (mg/L)", "id":"i_crp"},
    "thrus": {"type": "chk", "label": "Oral Thrush", "id":"i_thrus"},
    "rash": {"type": "chk", "label": "Butterfly Rash", "id":"i_rash"},
    "wast": {"type": "chk", "label": "Wasting Syndrome", "id":"i_wast"},
    "arth": {"type": "chk", "label": "Symmetric Joint Pain", "id":"i_arth"},
    "rayn": {"type": "chk", "label": "Raynaud's Phenomenon", "id":"i_rayn"},
    "sicca": {"type": "chk", "label": "Dry Eyes/Mouth", "id":"i_sicca"},
    "lymph": {"type": "chk", "label": "Generalized Nodes", "id":"i_lymph"},
    "splen": {"type": "chk", "label": "Splenomegaly", "id":"i_splen"},
    "petec": {"type": "chk", "label": "Petechiae/Purpura", "id":"i_petec"},
    "myalg": {"type": "chk", "label": "Chronic Myalgia", "id":"i_myalg"},
    "uvee": {"type": "chk", "label": "Uveitis/Eye Redness", "id":"i_uvee"},
    "alope": {"type": "chk", "label": "Alopecia Areata", "id":"i_alope"},
    "apht": {"type": "chk", "label": "Aphthous Ulcers", "id":"i_apht"},
    "seros": {"type": "chk", "label": "Serositis/Pleurisy", "id":"i_seros"},
    "vascu": {"type": "chk", "label": "Vasculitic Livedo", "id":"i_vascu"},
    "pneum": {"type": "chk", "label": "Opportunistic Pneumonia", "id":"i_pneum"},
    "shing": {"type": "chk", "label": "Recurrent Shingles", "id":"i_shing"},
    "cytop": {"type": "chk", "label": "Cytopenia signs", "id":"i_cytop"},
    "neuro": {"type": "chk", "label": "Peripheral Neuropathy", "id":"i_neuro"},
}

endo_defs = {
    "hba1c": {"type": "num", "label": "HbA1c (%)", "id":"e_hba1c"},
    "fbg": {"type": "num", "label": "Fasting Blood Glucose (mmol/L)", "id":"e_fbg"},
    "tsh": {"type": "num", "label": "TSH Level (mIU/L)", "id":"e_tsh"},
    "ft4": {"type": "num", "label": "Free T4 (ng/dL)", "id":"e_ft4"},
    "t3": {"type": "num", "label": "Total T3 (ng/dL)", "id":"e_t3"},
    "cort": {"type": "num", "label": "Morning Cortisol (µg/dL)", "id":"e_cort"},
    "pth": {"type": "num", "label": "Parathyroid Hormone (pg/mL)", "id":"e_pth"},
    "vitd": {"type": "num", "label": "Vitamin D (25-OH) (ng/mL)", "id":"e_vitd"},
    "igf1": {"type": "num", "label": "IGF-1 Level (ng/mL)", "id":"e_igf1"},
    "testo": {"type": "num", "label": "Total Testosterone (ng/dL)", "id":"e_testo"},
    "poly": {"type": "chk", "label": "Polyuria (Frequent Peeing)", "id":"e_poly"},
    "polyd": {"type": "chk", "label": "Polydipsia (Excess Thirst)", "id":"e_polyd"},
    "wt_loss": {"type": "chk", "label": "Unexplained Weight Loss", "id":"e_wt_loss"},
    "wt_gain": {"type": "chk", "label": "Rapid Weight Gain", "id":"e_wt_gain"},
    "hirs": {"type": "chk", "label": "Hirsutism", "id":"e_hirs"},
    "heat_int": {"type": "chk", "label": "Heat Intolerance", "id":"e_heat_int"},
    "cold_int": {"type": "chk", "label": "Cold Intolerance", "id":"e_cold_int"},
    "exoph": {"type": "chk", "label": "Exophthalmos (Bulging Eyes)", "id":"e_exoph"},
    "goiter": {"type": "chk", "label": "Visible Goiter", "id":"e_goiter"},
    "tremor": {"type": "chk", "label": "Fine Hand Tremors", "id":"e_tremor"},
    "acanth": {"type": "chk", "label": "Acanthosis Nigricans", "id":"e_acanth"},
    "moon": {"type": "chk", "label": "Moon Facies", "id":"e_moon"},
    "striae": {"type": "chk", "label": "Purple Striae", "id":"e_striae"},
    "gyno": {"type": "chk", "label": "Gynecomastia", "id":"e_gyno"},
    "fatigue": {"type": "chk", "label": "Chronic Fatigue", "id":"e_fatigue"},
}

pedia_defs = {
    "weight": {"type": "num", "label": "Weight (kg)", "id":"p_weight"},
    "height": {"type": "num", "label": "Height/Length (cm)", "id":"p_height"},
    "hc": {"type": "num", "label": "Head Circumference (cm)", "id":"p_hc"},
    "temp": {"type": "num", "label": "Body Temperature (°C)", "id":"p_temp"},
    "spo2": {"type": "num", "label": "SpO2 (%)", "id":"p_spo2"},
    "rr": {"type": "num", "label": "Respiratory Rate (breaths/min)", "id":"p_rr"},
    "apgar": {"type": "num", "label": "APGAR Score (0–10)", "id":"p_apgar"},
    "bili": {"type": "num", "label": "Total Bilirubin (mg/dL)", "id":"p_bili"},
    "growth": {"type": "chk", "label": "Growth Percentile", "id":"p_growth"},
    "age_mo": {"type": "num", "label": "Age (Months)", "id":"p_age_mo"},
    "poor_f": {"type": "chk", "label": "Poor Feeding", "id":"p_poor_f"},
    "leth": {"type": "chk", "label": "Lethargy", "id":"p_leth"},
    "irrit": {"type": "chk", "label": "Inconsolable Crying", "id":"p_irrit"},
    "font": {"type": "chk", "label": "Bulging Fontanelle", "id":"p_font"},
    "retr": {"type": "chk", "label": "Chest Retractions", "id":"p_retr"},
    "strid": {"type": "chk", "label": "Stridor", "id":"p_strid"},
    "jaund": {"type": "chk", "label": "Neonatal Jaundice", "id":"p_jaund"},
    "rash_d": {"type": "chk", "label": "Diaper Dermatitis", "id":"p_rash_d"},
    "milstn": {"type": "chk", "label": "Delayed Milestones", "id":"p_milstn"},
    "cyan_c": {"type": "chk", "label": "Central Cyanosis", "id":"p_cyan_c"},
    "vomit": {"type": "chk", "label": "Projectile Vomiting", "id":"p_vomit"},
    "dehyd": {"type": "chk", "label": "Sunken Eyes/Fontanelle", "id":"p_dehyd"},
    "ear_p": {"type": "chk", "label": "Tugging at Ears", "id":"p_ear_p"},
    "vacc": {"type": "chk", "label": "Up-to-date Vaccines", "id":"p_vacc"},
    "mumb": {"type": "chk", "label": "Umbilical Hernia", "id":"p_mumb"},
}

derm_defs = {
    "lesion_s": {"type": "num", "label": "Lesion Size (mm)", "id":"d_lesion_s"},
    "ph_level": {"type": "num", "label": "Skin pH", "id":"d_ph_level"},
    "pruritus": {"type": "chk", "label": "Severe Itching (Pruritus)", "id":"d_pruritus"},
    "erythema": {"type": "chk", "label": "Redness (Erythema)", "id":"d_erythema"},
    "vesicles": {"type": "chk", "label": "Blistering/Vesicles", "id":"d_vesicles"},
    "scaling": {"type": "chk", "label": "Scaling/Flaking", "id":"d_scaling"},
    "pigment": {"type": "chk", "label": "Hyperpigmentation", "id":"d_pigment"},
    "asym": {"type": "chk", "label": "Asymmetrical Border", "id":"d_asym"},
    "u_healing": {"type": "chk", "label": "Non-healing Ulcer", "id":"d_u_healing"},
}

psych_defs = {
    "phq9": {"type": "num", "label": "PHQ-9 Score", "id":"p_phq9"},
    "gad7": {"type": "num", "label": "GAD-7 Score", "id":"p_gad7"},
    "sleep_h": {"type": "num", "label": "Hours of Sleep", "id":"p_sleep_h"},
    "anhedonia": {"type": "chk", "label": "Loss of Interest", "id":"p_anhedonia"},
    "anxiety": {"type": "chk", "label": "Acute Anxiety", "id":"p_anxiety"},
    "halluc": {"type": "chk", "label": "Hallucinations", "id":"p_halluc"},
    "mania": {"type": "chk", "label": "Pressured Speech/Mania", "id":"p_mania"},
    "suicide": {"type": "chk", "label": "Suicidal Ideation", "id":"p_suicide"},
    "memory": {"type": "chk", "label": "Cognitive Impairment", "id":"p_memory"},
}

neph_defs = {
    "creat": {"type": "num", "label": "Serum Creatinine (mg/dL)", "id":"n_creat"},
    "egfr": {"type": "num", "label": "eGFR (mL/min/1.73 m²)", "id":"n_egfr"},
    "bun": {"type": "num", "label": "BUN (mg/dL)", "id":"n_bun"},
    "k_level": {"type": "num", "label": "Potassium (K+) (mmol/L)", "id":"n_k_level"},
    "u_alb": {"type": "num", "label": "Albumin/Creat Ratio (mg/g)", "id":"n_u_alb"},
    "hematuria": {"type": "chk", "label": "Blood in Urine", "id":"n_hematuria"},
    "foamy": {"type": "chk", "label": "Foamy Urine", "id":"n_foamy"},
    "oliguria": {"type": "chk", "label": "Decreased Output", "id":"n_oliguria"},
    "u_edema": {"type": "chk", "label": "Periorbital Edema", "id":"n_u_edema"},
    "u_itch": {"type": "chk", "label": "Uremic Pruritus", "id":"n_u_itch"},
}

hema_defs = {
    "hb": {"type": "num", "label": "Hemoglobin (g/dL)", "id":"h_hb"},
    "wbc": {"type": "num", "label": "White Cell Count (×10³/µL)", "id":"h_wbc"},
    "plt": {"type": "num", "label": "Platelet Count (×10³/µL)", "id":"h_plt"},
    "mcv": {"type": "num", "label": "Mean Corpuscular Vol (fL)", "id":"h_mcv"},
    "inr": {"type": "num", "label": "INR/Protime (ratio)", "id":"h_inr"},
    "ferritin": {"type": "num", "label": "Serum Ferritin (ng/mL)", "id":"h_ferritin"},
    "pallor": {"type": "chk", "label": "Conjunctival Pallor", "id":"h_pallor"},
    "petechiae": {"type": "chk", "label": "Petechiae/Bruising", "id":"h_petechiae"},
    "lymph": {"type": "chk", "label": "Lymphadenopathy", "id":"h_lymph"},
    "spleno": {"type": "chk", "label": "Splenomegaly", "id":"h_spleno"},
    "epistax": {"type": "chk", "label": "Frequent Nosebleeds", "id":"h_epistax"},
}

# ------------ Create tabs and inputs -------------
tab_names = [
    ("metabolism", "🧪 Metabolism", vital_defs),
    ("cardiac", "❤️ Cardiac", cardiac_defs),
    ("oncology", "🧬 Oncology", onco_defs),
    ("neurology", "🧠 Neurology", neural_defs),
    ("gynecology", "👩 Gynecology", gynae_defs),
    ("immunology", "🛡️ Immunology", immuno_defs),
    ("endocrinology", "🦋 Endocrinology", endo_defs),
    ("pediatric", "👶 Pediatric", pedia_defs),
    ("dermatology", "🧴 Dermatology", derm_defs),
    ("psychiatry", "🧠 Psychiatry", psych_defs),
    ("nephrology", "💧 Nephrology", neph_defs),
    ("hematology", "🩸 Hematology", hema_defs),
]

if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False

try:
    expander_target = expander_placeholder
except NameError:
    expander_target = st.empty()

# ------------ Analysis page -------------
if page == "analysis":
    render_navbar()
    st.markdown("<div id='page-top'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="stepper">
            <div class="stepper-step">1. Profile</div>
            <div class="stepper-step active">2. Analysis</div>
            <div class="stepper-step">3. Chat</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_analysis_chat_styles()
    st.markdown("<div class='analysis-tool-shell'>", unsafe_allow_html=True)
    output = []  # Initialize output list

    # keep patient values local in analysis
    patient_name = st.session_state.patient_name or "Unknown"
    patient_age = st.session_state.patient_age or "N/A"
    patient_gender = st.session_state.patient_gender or "N/A"

    if "chat_page" not in st.session_state:
        st.session_state.chat_page = None


    st.markdown(
        f"""
        <div class='dashboard-shell'>
            <div class='dashboard-top-grid'>
                <div class='glass-card'>
                    <div class='card-header'><span class='section-icon'>📊</span> Insights console</div>
                    <div class='profile-row'>
                        <div class='avatar'></div>
                        <div>
                            <div class='profile-name'>{patient_name}</div>
                            <div class='profile-meta'>Age: {patient_age} · Gender: {patient_gender}</div>
                            <div class='status-badge'>Active</div>
                        </div>
                    </div>
                    <div class='metrics-grid'>
                        <div class='metric-pill'><strong>{len(st.session_state.uploaded_images)} assets</strong><span><br>Uploaded files ready for review.</br></span></div>
                        <div class='metric-pill'><strong>{len(tab_names)} categories</strong><span>   Structured data sections available.   </span></div>
                    </div>
                </div>
                <div class='glass-card action-card'>
                    <div class='card-header'><span class='section-icon'>⚡</span> Workspace actions</div>
                    <div class='profile-meta'>Run analysis, save progress, or export insights from a polished dashboard experience.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button("⬅️ Back to Profile", key="back_to_profile", on_click=set_page, args=("profile",))
    expander_placeholder = st.empty()

    def render_chat_options():
        st.markdown(
            """
            <div class='assistant-experience-section'>
                <div class='assistant-experience-header'>
                    <div class='assistant-experience-title'>Choose Your AI Experience</div>
                    <div class='assistant-experience-subtitle'>Select how you want to interact with the system</div>
                    <div class='assistant-experience-underline'></div>
                </div>
                <div class='assistant-option-grid'>
                    <div class='assistant-option-card recommended'>
                        <div class='assistant-option-icon'>👩‍⚕️</div>
                        <div class='assistant-option-title'>Insights Advisor</div>
                        <div class='assistant-option-desc'>Long-form reasoning, structured recommendations, and guided interpretation.</div>
                        <div class='assistant-option-meta'>
                            <div class='option-badge'>Recommended</div>
                        </div>
                        <div class='assistant-option-action'></div>
                    </div>
                    <div class='assistant-option-card'>
                        <div class='assistant-option-icon'>⚡</div>
                        <div class='assistant-option-title'>Quick Summary</div>
                        <div class='assistant-option-desc'>Short insights, fast clarifications, and high-level findings.</div>
                        <div class='assistant-option-meta'>
                            <div class='option-badge'>Fast response</div>
                        </div>
                        <div class='assistant-option-action'></div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Replaced st.columns with responsive flex layout for assistant choice buttons
        st.markdown('<div class="responsive-assistant-grid">', unsafe_allow_html=True)
        st.button("Open Insights Advisor", key="choose_medical_assistant", on_click=launch_chat, args=("medical",))
        st.button("Open Quick Summary", key="choose_quick_assistant", on_click=launch_chat, args=("quick",))
        st.markdown('</div>', unsafe_allow_html=True)


    st.markdown("<div class='tool-grid-wrap'>", unsafe_allow_html=True)
    st.markdown('<div class="analysis-layout">', unsafe_allow_html=True)
    st.markdown('<div class="col-left">', unsafe_allow_html=True)
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("### 📥 Clinical Inputs")
    st.markdown(
        """
        <div class='glass-card'>
            <div class='card-header'><span class='section-icon'>🧩</span> Intake dashboard</div>
            <p class='profile-meta'>Choose a category, enter your core data, and use the dashboard to generate concise insights.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with expander_placeholder.expander("Clinical Intake Dashboard", expanded=True):
        tabs_objs = st.tabs([x[1] for x in tab_names])
        collected = {}

        for (tab_key, tab_label, defs), tab_obj in zip(tab_names, tabs_objs):
            with tab_obj:
                collected[tab_key] = make_inputs(tab_obj, defs)
        any_section_data = any(
            any(value is not None and value is not False and value != "" for value in section.values())
            for section in [
                collected.get("metabolism", {}),
                collected.get("cardiac", {}),
                collected.get("oncology", {}),
                collected.get("neurology", {}),
                collected.get("gynecology", {}),
                collected.get("immunology", {}),
                collected.get("endocrinology", {}),
                collected.get("pediatric", {}),
                collected.get("dermatology", {}),
                collected.get("psychiatry", {}),
                collected.get("nephrology", {}),
                collected.get("hematology", {}),
            ]
        ) or bool(st.session_state.uploaded_images) or bool(st.session_state.manual_symptoms.strip())

        st.markdown(
            """
            <div class='upload-panel panel-card'>
                <div class='panel-title'>Upload clinical images</div>
                <p class='panel-subtitle'>Drag and drop scans, photos, pathology images, or capture a photo directly from your camera for the AI-assisted review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        camera_image = None
        if hasattr(st, "camera_input"):
            camera_image = st.camera_input(
                "Capture an image from your camera",
                key="camera_capture",
                help="Use your device camera to upload a photo directly into the diagnostic workflow.",
            )
            if camera_image:
                existing_names = [getattr(img, "name", None) for img in st.session_state.uploaded_images]
                if getattr(camera_image, "name", None) not in existing_names:
                    st.session_state.uploaded_images.append(camera_image)

        uploaded = st.file_uploader(
            "Upload wound photos, X-ray plates, or other scans",
            type=["png", "jpg", "jpeg", "bmp", "tiff"],
            accept_multiple_files=True,
            key="uploaded_image_files",
            help="Optional: upload patient imaging for reference in the diagnostic report.",
        )
        if uploaded:
            next_images = list(uploaded)
            for img in st.session_state.uploaded_images:
                if all(getattr(img, "name", None) != getattr(new_img, "name", None) for new_img in next_images):
                    next_images.append(img)
            st.session_state.uploaded_images = next_images

        if st.session_state.uploaded_images:
            st.markdown("**Preview uploaded images:**")
            st.markdown('<div class="responsive-image-grid">', unsafe_allow_html=True)
            for idx, img in enumerate(st.session_state.uploaded_images):
                st.image(img, caption=img.name, width=300)
                st.button(
                    "Remove",
                    key=f"remove_uploaded_image_{idx}",
                    on_click=remove_uploaded_image,
                    args=(idx,),
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(
                f"<div class='hint-box'>Uploaded {len(st.session_state.uploaded_images)} file(s) received. They will be included in the generated report.</div>",
                unsafe_allow_html=True,
            )
            st.button("Clear all uploaded images", key="clear_uploaded_images", on_click=clear_uploaded_images)

        manual_symptom_text = st.text_area(
            "Manual symptom labels / clinical complaints",
            value=st.session_state.manual_symptoms,
            placeholder="e.g. fever, chest pain, skin rash, fatigue, night sweats",
            help="Enter symptoms or problem labels when structured measurements are not available.",
            key="manual_symptoms",
            height=140,
        ).strip()

        if manual_symptom_text:
            st.markdown(
                f"<div class='hint-box'>Manual symptom input captured. You can run analysis using symptom labels only.</div>",
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)  # close input-section
        st.markdown("<div class='action-section'>", unsafe_allow_html=True)
        st.markdown("### ⚡ Actions")
        st.markdown(
            "<div class='analysis-action-bar'><div class='action-copy'>Primary action will activate once at least one clinical input, manual symptom text, or image is provided.</div></div>",
            unsafe_allow_html=True,
        )
        # Replaced st.columns with responsive flex layout for action buttons
        st.markdown('<div class="responsive-action-bar-grid">', unsafe_allow_html=True)
        st.button(
            "Run Analysis",
            key="generate_analysis",
            disabled=not any_section_data,
            on_click=request_analysis,
        )
        st.button("Save Draft", key="save_draft")
        st.button("Reset", key="reset_analysis")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # close action-section

        if st.session_state.get("analysis_output", "").strip():
            st.markdown("<div class='output-section'>", unsafe_allow_html=True)
            st.markdown("### 📋 Results")
            report_text = st.session_state.analysis_output
            st.markdown(
                """
                <div class='analysis-report-box'>
                    <div class='report-header'>
                        <div>
                            <div class='report-title'>Nirnay Diagnostics Report</div>
                            <div class='report-subtitle'>Structured findings and follow-up guidance generated from the clinical intake.</div>
                        </div>
                        <div class='report-badge'>Ready</div>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            # Replaced st.columns with responsive flex layout for download button
            st.markdown('<div class="responsive-download-grid">', unsafe_allow_html=True)
            st.download_button(
                "Download Report",
                report_text,
                file_name="nirnay_diagnostics_report.txt",
                mime="text/plain",
                key="download_report",
            )
            st.markdown('</div>', unsafe_allow_html=True)
            if st.session_state.get("uploaded_image_report", "").strip():
                report_html = html.escape(st.session_state.uploaded_image_report).replace("\n", " ")
                st.markdown(
                    f"""
                    <div class='upload-report-hover'>
                        <span class='upload-report-trigger'>Hover to view uploaded image report</span>
                        <div class='upload-report-card'>{report_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            for line in report_text.splitlines():
                safe_line = html.escape(line)
                if line.startswith("==="):
                    line_class = "heading"
                elif line.startswith("[CRITICAL]"):
                    line_class = "critical"
                elif line.startswith("[ALERT]"):
                    line_class = "alert"
                elif line.startswith("[!]"):
                    line_class = "warning"
                else:
                    line_class = "ok"
                st.markdown(f"<div class='result-line {line_class}'>{safe_line}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)  # close output-section

        st.markdown('</div>', unsafe_allow_html=True)  # close col-left
        st.markdown('<div class="col-right">', unsafe_allow_html=True)
        st.markdown("<div class='assistant-section'>", unsafe_allow_html=True)
        st.markdown("### 🤖 AI Assistant")
        st.markdown(
            """
            <div class='assistant-panel sticky'>
                <div class='assistant-title'>AI Assistant</div>
                <div class='assistant-chip-row'>
                    <span class='assistant-chip'>Diagnosis</span>
                    <span class='assistant-chip'>Risk</span>
                    <span class='assistant-chip'>Recommendations</span>
                </div>
                <div class='assistant-card'>
                    <h4>Suggested prompts</h4>
                    <ul>
                        <li>"Summarize the most urgent clinical findings."</li>
                        <li>"What are the top three risk factors for this patient?"</li>
                        <li>"Recommend the next diagnostic step."</li>
                    </ul>
                </div>
                <div class='assistant-card'>
                    <h4>Mini chat</h4>
                    <p>Ask the AI for a concise clinical interpretation of any abnormal metric or uploaded image.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_chat_options()
        st.markdown("</div>", unsafe_allow_html=True)  # close assistant-section
        st.markdown('</div>', unsafe_allow_html=True)  # close col-right
        st.markdown('</div>', unsafe_allow_html=True)  # close analysis-layout
        st.markdown("</div>", unsafe_allow_html=True)  # close tool-grid-wrap
        st.markdown("</div>", unsafe_allow_html=True)  # close analysis-tool-shell

v_checks = collected.get("metabolism", {})
c_checks = collected.get("cardiac", {})
o_checks = collected.get("oncology", {})
n_checks = collected.get("neurology", {})
g_checks = collected.get("gynecology", {})
i_checks = collected.get("immunology", {})
endo_checks = collected.get("endocrinology", {})
ped_checks = collected.get("pediatric", {})
derm_checks = collected.get("dermatology", {})
psych_checks = collected.get("psychiatry", {})
neph_checks = collected.get("nephrology", {})
hem_checks = collected.get("hematology", {})

metabolic_has_data = has_data(v_checks.values())
cardiac_has_data = has_data(c_checks.values())
onco_has_data = has_data(o_checks.values())
neural_has_data = has_data(n_checks.values())
gynae_has_data = has_data(g_checks.values())
immuno_has_data = has_data(i_checks.values())
endo_has_data = has_data(endo_checks.values())
ped_has_data = has_data(ped_checks.values())
derm_has_data = has_data(derm_checks.values())
psych_has_data = has_data(psych_checks.values())
neph_has_data = has_data(neph_checks.values())
hem_has_data = has_data(hem_checks.values())

any_section_data = any(
    any(value is not None and value is not False and value != "" for value in section.values())
    for section in [
        v_checks,
        c_checks,
        o_checks,
        n_checks,
        g_checks,
        i_checks,
        endo_checks,
        ped_checks,
        derm_checks,
        psych_checks,
        neph_checks,
        hem_checks,
    ]
) or bool(st.session_state.manual_symptoms.strip())

manual_symptom_text = st.session_state.manual_symptoms.strip()

output = []

if manual_symptom_text:
    output.append("\n=== 📝 MANUAL SYMPTOM INPUT ===")
    output.append(f"[+] Manual symptom labels: {manual_symptom_text}")
    if not any(
        any(value is not None and value is not False and value != "" for value in section.values())
        for section in [
            v_checks,
            c_checks,
            o_checks,
            n_checks,
            g_checks,
            i_checks,
            endo_checks,
            ped_checks,
            derm_checks,
            psych_checks,
            neph_checks,
            hem_checks,
        ]
    ) and not st.session_state.uploaded_images:
        output.append("[!] MANUAL: Symptom-only intake was used. Review these symptoms with a clinician and use them as a preliminary clinical problem list.")

if metabolic_has_data:
    output.append("\n=== 🧪 METABOLIC ANALYSIS ===")
    
glc, a1c = val("f_glc", v_checks), val("a1c", v_checks)
if metabolic_has_data and ((glc and glc > 125) or (a1c and a1c > 6.4)):
    output.append("[!] METABOLIC: Type II Diabetes. Strict Glycemic Control.")
if metabolic_has_data and glc and glc > 180:
    output.append("[CRITICAL] Hyperglycemic Crisis Risk! Immediate medical attention required.")

uric = val("uric", v_checks)
if metabolic_has_data and uric and uric > 7.0:
    output.append("[!] METABOLIC: Hyperuricemia(Too much Uric Acid) - Gout Risk. Low-Purine Diet advised.")

ins = val("ins", v_checks)
if metabolic_has_data and ins and ins > 20:
    output.append("[!] METABOLIC: Insulin Resistance detected. Monitor for Metabolic Syndrome.")

tsh, t3, t4 = val("tsh", v_checks), val("t3", v_checks), val("t4", v_checks)
if metabolic_has_data and ((tsh and tsh > 4.0) or (t3 and t3 < 0.8) or (t4 and t4 < 0.9)):
    output.append("[!] METABOLIC: Hypothyroidism detected. Iodine-rich diet advised.")
elif metabolic_has_data and ((tsh and tsh < 0.4) or (t3 and t3 > 2.0) or (t4 and t4 > 2.0)):
    output.append("[!] METABOLIC: Hyperthyroidism detected. Avoid Excess Iodine.")

crea = val("crea", v_checks)
if metabolic_has_data and crea and crea > 1.3:
    output.append("[CRITICAL] METABOLIC: Renal Impairment detected. Immediate Nephrology consult advised.")

eGFR = val("egfr", v_checks)
if metabolic_has_data and eGFR and eGFR < 60:
    output.append("[CRITICAL] METABOLIC: Chronic Kidney Disease Stage 3+. Urgent Nephrology referral needed.")

alt, ast = val("alt", v_checks), val("ast", v_checks)
if metabolic_has_data and ((alt and alt > 56) or (ast and ast > 40)):
    output.append("[!] METABOLIC: Hepatic Dysfunction detected. Avoid Alcohol and Hepatotoxins.")

ggt = val("ggt", v_checks)
if metabolic_has_data and ggt and ggt > 60:
    output.append("[!] METABOLIC: Biliary Obstruction risk. Further Hepatobiliary evaluation recommended.")

bmi = val("bmi", v_checks)
if metabolic_has_data and bmi and bmi >= 30:
    output.append("[!] METABOLIC: Obesity detected. Weight Reduction Program advised.")

temp = val("temp", v_checks)
if metabolic_has_data and temp and temp > 37.5:
    output.append("[!] METABOLIC: Low-Grade Fever detected. Monitor for Infections or Inflammatory conditions.")

urin = v_checks.get("urin")
if metabolic_has_data and urin:
    output.append("[!] METABOLIC: An unequenchable need to drink water detected.")
poly = v_checks.get("poly")
if metabolic_has_data and poly:
    output.append("[!] METABOLIC: Frequent urination problem detected. ")
if metabolic_has_data and poly and urin:
    output.append("[!] METABOLIC: Classic Hyperglycemia Symptoms. Prioritize Diabetes Evaluation.")

fatg = v_checks.get("fatg")
if metabolic_has_data and fatg and poly and urin:
    output.append("[!] METABOLIC: High Suspicion for Diabetes Mellitus. Expedite Diagnostic Workup.")

crave = v_checks.get("crave")
if metabolic_has_data and crave and poly and urin:
    output.append("[!] METABOLIC: Sugar Cravings with Hyperglycemia Symptoms. Early Diabetes Screening advised.")

heal = v_checks.get("heal")
if metabolic_has_data and heal and poly and urin:
    output.append("[!] METABOLIC: Impaired Wound Healing with Hyperglycemia Symptoms. Urgent Diabetes Assessment needed.")

blur = v_checks.get("blur")
if metabolic_has_data and blur and poly and urin:
    output.append("[!] METABOLIC: Blurred Vision with Hyperglycemia Symptoms. Immediate Ophthalmologic and Diabetes Evaluation.")

oed = v_checks.get("oed")
if metabolic_has_data and oed and poly and urin:
    output.append("[!] METABOLIC: Ankle Oedema with Hyperglycemia Symptoms. Prompt Diabetes and Cardiac Assessment required.")

breath = v_checks.get("breath")
if metabolic_has_data and breath and poly and urin:
    output.append("[!] METABOLIC: Acetone Breath with Hyperglycemia Symptoms. Urgent Diabetes Evaluation for Ketoacidosis risk.")

ting = v_checks.get("ting")
if metabolic_has_data and ting and poly and urin:
    output.append("[!] METABOLIC: Peripheral Neuropathy with Hyperglycemia Symptoms. Expedite Diabetes Workup.")

hair = v_checks.get("hair")
if metabolic_has_data and hair and poly and urin:
    output.append("[!] METABOLIC: Brittle Hair/Nails with Hyperglycemia Symptoms. Early Diabetes Screening recommended.")

trop = val("trop", c_checks)
if cardiac_has_data:
    output.append("\n=== ❤️ CARDIAC ANALYSIS ===")
    
if cardiac_has_data and trop and trop > 0.04:
    output.append("[CRITICAL] CARDIAC: Myocardial Infarction detected.")
sys_v = val("sys", c_checks)
if cardiac_has_data and sys_v and sys_v > 140:
    output.append("[ALERT] CARDIAC: Hypertension. Sodium restriction advised.")
bnp = val("bnp", c_checks)
if cardiac_has_data and bnp and bnp > 100:
    output.append("[!] CARDIAC: Heart Failure risk detected.")
hscrp = val("hscrp", c_checks)
if cardiac_has_data and hscrp and hscrp > 3.0:
    output.append("[!] CARDIAC: Elevated Inflammatory Marker. Atherosclerosis risk increased.")
ldl = val("ldl", c_checks)
hdl = val("hdl", c_checks)
if cardiac_has_data and ((ldl and ldl > 130) or (hdl and hdl < 40)):
    output.append("[!] CARDIAC: Dyslipidemia detected. Lifestyle modification advised.")
trig = val("trig", c_checks)
if cardiac_has_data and trig and trig > 150:
    output.append("[!] CARDIAC: Hypertriglyceridemia detected. Diet and exercise recommended.")

angina = c_checks.get("angina")
if cardiac_has_data and angina:
    output.append("[ALERT] CARDIAC: Air Hunger detected. ")
ortho = c_checks.get("ortho")
if cardiac_has_data and ortho:
    output.append("[ALERT] CARDIAC: Positional Breathlessness detected.")
if cardiac_has_data and angina and ortho:
    output.append("[ALERT] CARDIAC: Congestive Heart Failure signs detected.")
pnd = c_checks.get("pnd")
if cardiac_has_data and angina and pnd:
    output.append("[ALERT] CARDIAC: Possible Ischemic Heart Disease with Heart Failure signs.")
edema = c_checks.get("edema")
if cardiac_has_data and angina and edema:
    output.append("[ALERT] CARDIAC: Advanced Heart Failure indications detected.")
palp = c_checks.get("palp")
if cardiac_has_data and angina and palp:
    output.append("[ALERT] CARDIAC: Arrhythmia risk with Ischemic symptoms.")
sync = c_checks.get("sync")
if cardiac_has_data and angina and sync:
    output.append("[ALERT] CARDIAC: Severe Cardiac Dysfunction suspected.")
cyan = c_checks.get("cyan")
if cardiac_has_data and angina and cyan:
    output.append("[ALERT] CARDIAC: Critical Hypoxia with Cardiac symptoms.")
jvp = c_checks.get("jvp")
if cardiac_has_data and angina and jvp:
    output.append("[ALERT] CARDIAC: Right Heart Failure signs detected.")
club = c_checks.get("club")
if cardiac_has_data and angina and club:
    output.append("[ALERT] CARDIAC: Chronic Hypoxia with Cardiac symptoms.")
claud = c_checks.get("claud")
if cardiac_has_data and angina and claud:
    output.append("[ALERT] CARDIAC: Peripheral Arterial Disease with Cardiac symptoms.")
cold = c_checks.get("cold")
if cardiac_has_data and angina and cold:
    output.append("[ALERT] CARDIAC: Severe Peripheral Hypoperfusion detected.")
murm = c_checks.get("murm")
if cardiac_has_data and angina and murm:
    output.append("[ALERT] CARDIAC: Valvular Heart Disease signs detected.")
cough = c_checks.get("cough")
if cardiac_has_data and angina and cough:
    output.append("[ALERT] CARDIAC: Pulmonary Edema with Cardiac symptoms.")
sweat = c_checks.get("sweat")
if cardiac_has_data and angina and sweat:
    output.append("[ALERT] CARDIAC: Acute Coronary Syndrome suspected.")
nausea = c_checks.get("nausea")
if cardiac_has_data and angina and nausea:
    output.append("[ALERT] CARDIAC: Inferior MI signs detected.")

if onco_has_data:
    output.append("\n===🧬 ONCOLOGY ANALYSIS ===")

psa = val("psa", o_checks)
if onco_has_data and psa and psa > 4.0:
    output.append("[ALERT] ONCO: Prostate Cancer risk detected.")
ca125 = val("ca125", o_checks)
if onco_has_data and ca125 and ca125 > 35:
    output.append("[ALERT] ONCO: Ovarian Cancer risk detected.")
cea = val("cea", o_checks)
if onco_has_data and cea and cea > 5.0:
    output.append("[ALERT] ONCO: Colorectal Cancer risk detected.")
afp = val("afp", o_checks)
if onco_has_data and afp and afp > 10.0:
    output.append("[ALERT] ONCO: Hepatocellular Carcinoma risk detected.")
ca19 = val("ca19", o_checks)
if onco_has_data and ca19 and ca19 > 37:
    output.append("[ALERT] ONCO: Pancreatic Cancer risk detected.")
ldh = val("ldh", o_checks)
if onco_has_data and ldh and ldh > 250:
    output.append("[ALERT] ONCO: Possible Tumor Lysis Syndrome or Metastatic Disease.")
size = val("size", o_checks)
if onco_has_data and size and size > 5.0:
    output.append("[ALERT] ONCO: Large Mass detected. Urgent Oncologic evaluation recommended.")
weight_o = val("weight", o_checks)
if onco_has_data and weight_o and weight_o > 10.0:
    output.append("[ALERT] ONCO: Significant Unintended Weight Loss. Cancer screening advised.")
mass = o_checks.get("mass")
node = o_checks.get("node")
if onco_has_data and mass and node:
    output.append("[ALERT] ONCO: Suspicious Mass with Lymphadenopathy. Expedite Biopsy and Imaging.")
meta = o_checks.get("meta")
if onco_has_data and mass and meta:
    output.append("[ALERT] ONCO: Possible Metastatic Disease. Urgent Oncologic referral needed.")
night = o_checks.get("night")
if onco_has_data and mass and night:
    output.append("[ALERT] ONCO: Systemic Cancer symptoms detected.")
hemopt = o_checks.get("hemopt")
if onco_has_data and mass and hemopt:
    output.append("[ALERT] ONCO: Pulmonary Malignancy signs detected.")
dysph = o_checks.get("dysph")
if onco_has_data and mass and dysph:
    output.append("[ALERT] ONCO: Possible Esophageal Cancer symptoms detected.")
change = o_checks.get("change")
if onco_has_data and mass and change:
    output.append("[ALERT] ONCO: Colorectal Cancer symptoms detected.")
mole = o_checks.get("mole")
if onco_has_data and mass and mole:
    output.append("[ALERT] ONCO: Melanoma risk with Evolving Mole detected.")
hema = o_checks.get("hema")
if onco_has_data and mass and hema:
    output.append("[ALERT] ONCO: Possible Urinary Tract Malignancy signs detected.")
ascit = o_checks.get("ascit")
if onco_has_data and mass and ascit:
    output.append("[ALERT] ONCO: Advanced Intra-Abdominal Malignancy suspected.")
jaund = o_checks.get("jaund")
if onco_has_data and mass and jaund:
    output.append("[ALERT] ONCO: Hepatobiliary or Pancreatic Cancer signs detected.")
fract = o_checks.get("fract")
if onco_has_data and mass and fract:
    output.append("[ALERT] ONCO: Possible Bone Metastasis with Pathological Fracture.")
cachex = o_checks.get("cachex")
if onco_has_data and mass and cachex:
    output.append("[ALERT] ONCO: Severe Cancer Cachexia suspected.")
pleur = o_checks.get("pleur")
if onco_has_data and pleur:
    output.append("[ALERT] ONCO: Lung Cancer suspected!")
anem = o_checks.get("anem")
if onco_has_data and anem:
    output.append("[ALERT] ONCO: Possible Hematologic Malignancy suspected!")
fev = o_checks.get("fev")
if onco_has_data and fev:
    output.append("[ALERT] ONCO: Possible Hidden Malignancy suspected!")
itch = o_checks.get("itch")
if onco_has_data and itch:
    output.append("[ALERT] ONCO: Possible Lymphoma suspected!")

if neural_has_data:
    output.append("\n===🧠 NEUROLOGY ANALYSIS ===")
if neural_has_data and n_checks["tonic"] and n_checks["post"]:
    output.append("[ALERT] NEURAL: Epilepsy Pattern detected.")
if neural_has_data and n_checks["trem"] and n_checks["rigi"]:
    output.append("[ALERT] NEURAL: Parkinsonian Syndrome suspected.")
if neural_has_data and n_checks["weak"] and n_checks["sens"]:
    output.append("[ALERT] NEURAL: Focal Neurological Deficit detected. Stroke evaluation advised.")
if neural_has_data and n_checks["memo"] and n_checks["cogn"]:
    output.append("[ALERT] NEURAL: Cognitive Impairment signs detected. Dementia workup recommended.")
if neural_has_data and n_checks["myo"] and n_checks["aura"]:
    output.append("[ALERT] NEURAL: Myoclonic Epilepsy suspected.")
if neural_has_data and n_checks["phot"] and n_checks["vert"]:
    output.append("[ALERT] NEURAL: Migraine Variant suspected.")
if neural_has_data and n_checks["dipl"] and n_checks["dysf"]:
    output.append("[ALERT] NEURAL: Brainstem Dysfunction signs detected.")
if neural_has_data and n_checks["hic"] and n_checks["radic"]:
    output.append("[ALERT] NEURAL: Raised Intracranial Pressure signs detected.")
if neural_has_data and n_checks["babin"] and n_checks["pupil"]:
    output.append("[ALERT] NEURAL: Upper Motor Neuron Lesion signs detected.")
if neural_has_data and n_checks["stare"] and n_checks["post"]:
    output.append("[ALERT] NEURAL: Absence Seizure with Post-Ictal signs detected.")
if neural_has_data and n_checks["atax"] and n_checks["trem"]:
    output.append("[ALERT] NEURAL: Cerebellar Dysfunction suspected.")
if neural_has_data and n_checks["slur"] and n_checks["weak"]:
    output.append("[ALERT] NEURAL: Possible Stroke or TIA signs detected.")
if neural_has_data and n_checks["neur"] and n_checks["sens"]:
    output.append("[ALERT] NEURAL: Peripheral Neuropathy signs detected.")
if neural_has_data and n_checks["migr"] and n_checks["tinn"]:
    output.append("[ALERT] NEURAL: Chronic Migraine with Tinnitus suspected.")
if neural_has_data and n_checks["memo"] and n_checks["migr"]:
    output.append("[ALERT] NEURAL: Migraine-Associated Cognitive Dysfunction detected.")
if  neural_has_data and n_checks["dipl"] and n_checks["vert"]:
    output.append("[ALERT] NEURAL: Brainstem or Vestibular Pathology suspected.")
if neural_has_data and n_checks["dysf"] and n_checks["cogn"]:
    output.append("[ALERT] NEURAL: Aphasia with Cognitive Impairment signs detected.")
if neural_has_data and n_checks["hic"] and n_checks["babin"]:
    output.append("[ALERT] NEURAL: Raised ICP with Upper Motor Neuron signs detected.")
if neural_has_data and n_checks["tonic"] and n_checks["aura"]:
    output.append("[ALERT] NEURAL: Generalized Tonic-Clonic Seizures with Aura suspected.")
if neural_has_data and n_checks["atax"] and n_checks["slur"]:
    output.append("[ALERT] NEURAL: Cerebellar Ataxia with Dysarthria signs detected.")
if neural_has_data and n_checks["weak"] and n_checks["neur"]:
    output.append("[ALERT] NEURAL: Focal Weakness with Neuralgia suspected.")
if neural_has_data and n_checks["trem"] and n_checks["memo"]:
    output.append("[ALERT] NEURAL: Parkinsonism with Cognitive Decline signs detected.")
if neural_has_data and n_checks["post"] and n_checks["cogn"]:
    output.append("[ALERT] NEURAL: Post-Ictal Cognitive Dysfunction suspected.")
if neural_has_data and n_checks["stare"] and n_checks["migr"]:
    output.append("[ALERT] NEURAL: Absence Seizures with Migraine features detected.")
if neural_has_data and n_checks["aura"] and n_checks["phot"]:
    output.append("[ALERT] NEURAL: Migraine with Aura and Photophobia suspected.")
if neural_has_data and n_checks["dipl"] and n_checks["hic"]:
    output.append("[ALERT] NEURAL: Diplopia with Raised ICP signs detected.")
if neural_has_data and n_checks["radic"] and n_checks["babin"]:
    output.append("[ALERT] NEURAL: Radicular Pain with Upper Motor Neuron signs detected.")
if neural_has_data and n_checks["tonic"] and n_checks["myo"]:
    output.append("[ALERT] NEURAL: Mixed Seizure Disorder suspected.")
if neural_has_data and n_checks["atax"] and n_checks["weak"]:
    output.append("[ALERT] NEURAL: Cerebellar Ataxia with Focal Weakness detected.")
if neural_has_data and n_checks["trem"] and n_checks["slur"]:
    output.append("[ALERT] NEURAL: Parkinsonism with Dysarthria signs detected.")
if neural_has_data and n_checks["memo"] and n_checks["hic"]:
    output.append("[ALERT] NEURAL: Cognitive Impairment with Raised ICP suspected.")
if neural_has_data and n_checks["dipl"] and n_checks["radic"]:
    output.append("[ALERT] NEURAL: Brainstem Dysfunction with Radicular Pain detected.")
if neural_has_data and n_checks["post"] and n_checks["neur"]:
    output.append("[ALERT] NEURAL: Post-Ictal Peripheral Neuropathy signs detected.")
if neural_has_data and n_checks["migr"] and n_checks["cogn"]:
    output.append("[ALERT] NEURAL: Migraine-Associated Cognitive Dysfunction suspected.")
if neural_has_data and n_checks["aura"] and n_checks["vert"]:
    output.append("[ALERT] NEURAL: Vestibular Migraine suspected.")
if neural_has_data and n_checks["dysf"] and n_checks["hic"]:
    output.append("[ALERT] NEURAL: Aphasia with Raised ICP signs detected.")
if neural_has_data and n_checks["babin"] and n_checks["pupil"]:
    output.append("[ALERT] NEURAL: Upper Motor Neuron Lesion with Pupillary Abnormalities detected.")

if gynae_has_data:
    output.append("\n===👩 GYNECOLOGY ANALYSIS ===")
if gynae_has_data and g_checks["pcos"]:
    output.append("[ALERT] GYNAE: PCOS Markers positive. Further endocrine evaluation recommended.")
if gynae_has_data and g_checks["endo"]:
    output.append("[ALERT] GYNAE: Endometriosis Pain reported. Pelvic ultrasound advised.")
if gynae_has_data and g_checks["lesi"] and g_checks["puru"]:
    output.append("[ALERT] GYNAE: Infectious Genital Ulcers with Purulent Discharge. STI screening recommended.")
if gynae_has_data and g_checks["amen"] and g_checks["dysme"]:
    output.append("[ALERT] GYNAE: Menstrual Irregularities detected. Hormonal profile evaluation advised.")
if gynae_has_data and g_checks["infert"]:
    output.append("[ALERT] GYNAE: Primary Infertility reported. Comprehensive fertility workup recommended.")
if gynae_has_data and g_checks["libi"]:
    output.append("[ALERT] GYNAE: Reduced Libido reported. Hormonal and Psychological evaluation advised.")
if gynae_has_data and g_checks["cyst"]:
    output.append("[ALERT] GYNAE: Ovarian Cyst signs detected. Pelvic imaging recommended.")
if gynae_has_data and g_checks["menop"]:
    output.append("[ALERT] GYNAE: Menopausal Symptoms reported. Hormone Replacement Therapy discussion advised.")
if gynae_has_data and g_checks["herp"] and g_checks["cand"]:
    output.append("[ALERT] GYNAE: Genital Herpes with Candidiasis signs detected. Antiviral and Antifungal treatment recommended.")
if gynae_has_data and g_checks["warta"] and g_checks["chan"]:
    output.append("[ALERT] GYNAE: Genital Warts with Chancre detected. Urgent STI evaluation advised.")
if gynae_has_data and g_checks["balan"] and g_checks["ureth"]:
    output.append("[ALERT] GYNAE: Balanitis with Urethritis signs detected. Urological consultation recommended.")
if gynae_has_data and g_checks["spot"] and g_checks["dyspa"]:
    output.append("[ALERT] GYNAE: Intermenstrual Spotting with Dyspareunia reported. Pelvic examination advised.")
if gynae_has_data and g_checks["pelv"]:
    output.append("[ALERT] GYNAE: Pelvic Inflammatory signs detected. Immediate antibiotic therapy recommended.")
if gynae_has_data and g_checks["mast"] and g_checks["bloat"]:
    output.append("[ALERT] GYNAE: Breast and Abdominal symptoms reported. Comprehensive gynecological evaluation advised.")
if gynae_has_data and g_checks["prola"]:
    output.append("[ALERT] GYNAE: Uterine Prolapse signs detected. Pelvic floor assessment recommended.")
if gynae_has_data and g_checks["sicca"]:
    output.append("[ALERT] GYNAE: Sjogren's Syndrome signs detected. Rheumatologic evaluation advised.")
if gynae_has_data and g_checks["lymph"]:
    output.append("[ALERT] GYNAE: Inguinal Lymphadenopathy detected. Further infectious and oncologic workup recommended.")

if immuno_has_data:
    output.append("\n===🛡️ IMMUNOLOGY ANALYSIS ===")
cd4 = val("cd4", i_checks)
if immuno_has_data and ((cd4 and cd4 < 200) or i_checks["thrus"]):
    output.append("[CRITICAL] IMMUNO: Severe immune deficiency/failure.")
ana = val("ana", i_checks)
if immuno_has_data and ana:
    output.append("[ALERT] IMMUNO: ANA positive. Further autoimmune evaluation recommended.")
esr = val("esr", i_checks)
if immuno_has_data and esr and esr > 20:
    output.append("[!] IMMUNO: Elevated ESR levels detected. Further inflammatory assessment recommended.")
wbc = val("wbc", i_checks)
if immuno_has_data and wbc and (wbc < 4000 or wbc > 11000):
    output.append("[!] IMMUNO: Abnormal WBC count detected. Further immunological evaluation advised.")
igg = val("igg", i_checks)
if immuno_has_data and igg and igg < 700:
    output.append("[!] IMMUNO: Hypogammaglobulinemia detected. Further immunological evaluation recommended.")
crp = val("crp", i_checks)
if immuno_has_data and crp and crp > 10:
    output.append("[!] IMMUNO: Elevated CRP levels detected. Possible inflammation or infection.")
rash = i_checks["rash"]
if immuno_has_data and rash:
    output.append("[!] IMMUNO: Butterfly Rash reported. Possible Lupus evaluation recommended.")
wast = i_checks["wast"]
if immuno_has_data and wast:
    output.append("[!] IMMUNO: Wasting Syndrome reported. Comprehensive evaluation advised.")
arth = i_checks["arth"]
if immuno_has_data and arth:
    output.append("[!] IMMUNO: Symmetric Joint Pain reported. Possible autoimmune arthritis evaluation recommended.")
rayn = i_checks["rayn"]
if immuno_has_data and rayn:
    output.append("[!] IMMUNO: Raynaud's Phenomenon reported. Further vascular evaluation advised.")
sicca = i_checks["sicca"]
if immuno_has_data and sicca:
    output.append("[!] IMMUNO: Sicca Symptoms reported. Possible Sjogren's Syndrome evaluation recommended.")
lymph = i_checks["lymph"]
if immuno_has_data and lymph:
    output.append("[!] IMMUNO: Lymphadenopathy detected. Further infectious and oncologic workup recommended.")
splen = i_checks["splen"]
if immuno_has_data and splen:
    output.append("[!] IMMUNO: Splenomegaly detected. Further hematologic evaluation advised.")
petec = i_checks["petec"]
if immuno_has_data and petec:
    output.append("[!] IMMUNO: Petechiae/Purpura reported. Possible platelet disorder evaluation recommended.")
myalg = i_checks["myalg"]
if immuno_has_data and myalg:
    output.append("[!] IMMUNO: Chronic Myalgia reported. Further immunological or infectious workup advised.")
uvee = i_checks["uvee"]
if immuno_has_data and uvee:
    output.append("[!] IMMUNO: Uveitis reported. Possible autoimmune or infectious etiology evaluation recommended.")
alope = i_checks["alope"]
if immuno_has_data and alope:
    output.append("[!] IMMUNO: Alopecia Areata reported. Possible autoimmune evaluation recommended.")
apht = i_checks["apht"]
if immuno_has_data and apht:
    output.append("[!] IMMUNO: Aphthous Ulcers reported. Possible autoimmune or inflammatory evaluation recommended.")
seros = i_checks["seros"]
if immuno_has_data and seros:
    output.append("[!] IMMUNO: Serositis reported. Possible autoimmune or infectious evaluation recommended.")
vascu = i_checks["vascu"]
if immuno_has_data and vascu:
    output.append("[!] IMMUNO: Vasculitic Livedo reported. Further rheumatologic evaluation advised.")
pneum = i_checks["pneum"]
if immuno_has_data and pneum:
    output.append("[!] IMMUNO: Opportunistic Pneumonia reported. Possible autoimmune or infectious evaluation recommended.")
shing = i_checks["shing"]
if immuno_has_data and shing:
    output.append("[!] IMMUNO: Recurrent Shingles reported. Possible reactivation of varicella zoster virus.")
cytop = i_checks["cytop"]
if immuno_has_data and cytop:
    output.append("[!] IMMUNO: Cytopenia signs reported. Possible hematologic disorder evaluation advised.")
neuro = i_checks["neuro"]
if immuno_has_data and neuro:
    output.append("[!] IMMUNO: Peripheral Neuropathy reported. Further neurological evaluation advised.")
if endo_has_data:
    output.append("\n===🦋 ENDOCRINOLOGY ANALYSIS ===")
hba1c = val("hba1c", endo_checks)
if endo_has_data and hba1c and hba1c >= 6.5:
    output.append("[ALERT] ENDOCRINE: Diabetes Mellitus likely. Glycemic control evaluation advised.")
fbg = val("fbg", endo_checks)
if endo_has_data and fbg and fbg >= 126:
    output.append("[ALERT] ENDOCRINE: Fasting Blood Glucose elevated. Diabetes screening recommended.")
tsh_e = val("tsh", endo_checks)
if endo_has_data and tsh_e and (tsh_e < 0.4 or tsh_e > 4.0):
    output.append("[ALERT] ENDOCRINE: Abnormal TSH levels detected. Thyroid function evaluation advised.")
ft4 = val("ft4", endo_checks)
if endo_has_data and ft4 and (ft4 < 0.8 or ft4 > 1.8):
    output.append("[ALERT] ENDOCRINE: Abnormal Free T4 levels detected. Thyroid disorder evaluation recommended.")
t3_e = val("t3", endo_checks)
if endo_has_data and t3_e and (t3_e < 80 or t3_e > 200):
    output.append("[ALERT] ENDOCRINE: Abnormal T3 levels detected. Further thyroid evaluation advised.")
cort = val("cort", endo_checks)
if endo_has_data and cort and (cort < 5 or cort > 25):
    output.append("[ALERT] ENDOCRINE: Abnormal Cortisol levels detected. Adrenal function evaluation recommended.")
pth = val("pth", endo_checks)
if endo_has_data and pth and (pth < 10 or pth > 65):
    output.append("[ALERT] ENDOCRINE: Abnormal PTH levels detected. Calcium metabolism evaluation advised.")
vitd = val("vitd", endo_checks)
if endo_has_data and vitd and vitd < 20:
    output.append("[ALERT] ENDOCRINE: Vitamin D Deficiency detected. Supplementation and bone health evaluation recommended.")
igf1 = val("igf1", endo_checks)
if endo_has_data and igf1 and (igf1 < 100 or igf1 > 300):
    output.append("[ALERT] ENDOCRINE: Abnormal IGF-1 levels detected. Growth hormone axis evaluation advised.")
testo = val("testo", endo_checks)
if endo_has_data and testo and (testo < 300 or testo > 1000):
    output.append("[ALERT] ENDOCRINE: Abnormal Testosterone levels detected. Further endocrine evaluation recommended.")
poly_e = endo_checks["poly"]
if endo_has_data and poly_e:
    output.append("[!] ENDOCRINE: Polyuria reported. Diabetes mellitus evaluation advised.")
polyd = endo_checks["polyd"]
if endo_has_data and polyd:
    output.append("[!] ENDOCRINE: Polydipsia reported. Diabetes mellitus evaluation advised.")
wt_loss = endo_checks["wt_loss"]
if endo_has_data and wt_loss:
    output.append("[!] ENDOCRINE: Unexplained Weight Loss reported. Further assessment advised.")
wt_gain = endo_checks["wt_gain"]
if endo_has_data and wt_gain:
    output.append("[!] ENDOCRINE: Unexplained Weight Gain reported. Further assessment advised.")
hirs_e = endo_checks["hirs"]
if endo_has_data and hirs_e:
    output.append("[!] ENDOCRINE: Hirsutism reported. Androgen excess evaluation recommended.")
heat_int = endo_checks["heat_int"]
if endo_has_data and heat_int:
    output.append("[!] ENDOCRINE: Heat Intolerance reported. Thyroid disorder evaluation recommended.")
cold_int = endo_checks["cold_int"]
if endo_has_data and cold_int:
    output.append("[!] ENDOCRINE: Cold Intolerance reported. Thyroid disorder evaluation recommended.")
exoph = endo_checks["exoph"]
if endo_has_data and exoph:
    output.append("[!] ENDOCRINE: Exophthalmos reported. Thyroid eye disease evaluation advised.")
goiter = endo_checks["goiter"]
if endo_has_data and goiter:
    output.append("[!] ENDOCRINE: Goiter detected. Thyroid function and structural evaluation recommended.")
tremor_e = endo_checks["tremor"]
if endo_has_data and tremor_e:
    output.append("[!] ENDOCRINE: Tremors reported. Possible thyroid or neurological evaluation advised.")
acanth = endo_checks["acanth"]
if endo_has_data and acanth:
    output.append("[!] ENDOCRINE: Acanthosis Nigricans detected. Insulin resistance evaluation recommended.")
moon = endo_checks["moon"]
if endo_has_data and moon:
    output.append("[!] ENDOCRINE: Moon Face appearance reported. Possible Cushing's syndrome evaluation advised.")
striae = endo_checks["striae"]
if endo_has_data and striae:
    output.append("[!] ENDOCRINE: Purple Striae detected. Possible Cushing's syndrome evaluation advised.")
gyno_e = endo_checks["gyno"]
if endo_has_data and gyno_e:
    output.append("[!] ENDOCRINE: Gynecomastia reported. Hormonal imbalance evaluation recommended.")
fatigue_e = endo_checks["fatigue"]
if endo_has_data and fatigue_e:
    output.append("[!] ENDOCRINE: Persistent Fatigue reported. Comprehensive evaluation recommended.")

if ped_has_data:
    output.append("\n===👶 PEDIATRIC ANALYSIS ===")
weight_p = val("weight", ped_checks)
height_p = val("height", ped_checks)
if ped_has_data and weight_p and height_p:
    bmi_p = weight_p / ((height_p / 100) ** 2)
    if bmi_p < 14:
        output.append("[!] PEDIATRIC: Underweight status detected. Nutritional assessment advised.")
    elif bmi_p > 18.5:
        output.append("[!] PEDIATRIC: Overweight status detected. Dietary and lifestyle evaluation recommended.")
hc_p = val("hc", ped_checks)
if ped_has_data and hc_p and (hc_p < 45 or hc_p > 55):
    output.append("[!] PEDIATRIC: Abnormal Head Circumference detected. Further neurological evaluation advised.")
temp_p = val("temp", ped_checks)
if ped_has_data and temp_p and temp_p > 100.4:
    output.append("[!] PEDIATRIC: Fever detected. Possible infection evaluation recommended.")
spo2 = val("spo2", ped_checks)
if ped_has_data and spo2 and spo2 < 95:
    output.append("[!] PEDIATRIC: Low Oxygen Saturation detected. Respiratory evaluation advised.")
rr_p = val("rr", ped_checks)
if ped_has_data and rr_p and (rr_p < 20 or rr_p > 30):
    output.append("[!] PEDIATRIC: Abnormal Respiratory Rate detected. Further respiratory evaluation recommended.")
apgar = val("apgar", ped_checks)
if ped_has_data and apgar and apgar < 7:
    output.append("[!] PEDIATRIC: Low APGAR Score detected. Immediate neonatal assessment advised.")
bili = val("bili", ped_checks)
if ped_has_data and bili and bili > 12:
    output.append("[!] PEDIATRIC: Elevated Bilirubin levels detected. Jaundice evaluation recommended.")
growth = ped_checks["growth"]
if ped_has_data and growth:
    output.append("[!] PEDIATRIC: Growth Delay reported. Comprehensive pediatric evaluation advised.")
age_mo = val("age_mo", ped_checks)
if ped_has_data and age_mo is not None:
    if age_mo < 12:
        milestones = ped_checks["milstn"]
        if milestones:
            output.append("[!] PEDIATRIC: Developmental Milestone Delay reported in Infant. Early intervention recommended.")
    else:
        milestones = ped_checks["milstn"]
        if milestones:
            output.append("[!] PEDIATRIC: Developmental Milestone Delay reported in Toddler. Further developmental evaluation advised.")
poor_f = ped_checks["poor_f"]
if ped_has_data and poor_f:
    output.append("[!] PEDIATRIC: Poor Feeding reported. Nutritional and medical assessment recommended.")
leth = ped_checks["leth"]
if ped_has_data and leth:
    output.append("[!] PEDIATRIC: Lethargy reported. Further medical evaluation advised.")
irrit = ped_checks["irrit"]
if ped_has_data and irrit:
    output.append("[!] PEDIATRIC: Irritability reported. Possible underlying medical condition evaluation recommended.")
font = ped_checks["font"]
if ped_has_data and font:
    output.append("[!] PEDIATRIC: Bulging Fontanelle detected. Possible increased intracranial pressure evaluation advised.")
retr = ped_checks["retr"]
if ped_has_data and retr:
    output.append("[!] PEDIATRIC: Chest Retractions observed. Respiratory distress evaluation recommended.")
strid = ped_checks["strid"]
if ped_has_data and strid:
    output.append("[!] PEDIATRIC: Stridor observed. Airway obstruction evaluation recommended.")
jaund_p = ped_checks["jaund"]
if ped_has_data and jaund_p:
    output.append("[!] PEDIATRIC: Jaundice reported. Further hepatic evaluation recommended.")
rash_d = ped_checks["rash_d"]
if ped_has_data and rash_d:
    output.append("[!] PEDIATRIC: Rash reported. Possible infectious or allergic evaluation advised.")
cyan_c = ped_checks["cyan_c"]
if ped_has_data and cyan_c:
    output.append("[!] PEDIATRIC: Central Cyanosis signs detected. Cardiac evaluation advised.")
vomit = ped_checks["vomit"]
if ped_has_data and vomit:
    output.append("[!] PEDIATRIC: Persistent Vomiting reported. Further gastrointestinal evaluation recommended.")
dehyd = ped_checks["dehyd"]
if ped_has_data and dehyd:
    output.append("[!] PEDIATRIC: Signs of Dehydration observed. Immediate medical assessment advised.")
ear_p = ped_checks["ear_p"]
if ped_has_data and ear_p:
    output.append("[!] PEDIATRIC: Ear Pain reported. Possible otitis media evaluation recommended.")
vacc = ped_checks["vacc"]
if ped_has_data and vacc:
    output.append("[!] PEDIATRIC: Incomplete Vaccination status reported. Immunization schedule review advised.")
mumb = ped_checks["mumb"]
if ped_has_data and mumb:
    output.append("[!] PEDIATRIC: Umbilical Hernia reported. Surgical consultation advised.")
if derm_has_data:
    output.append("\n===🧴 DERMATOLOGY ANALYSIS ===")
lesion_s = val("lesion_s", derm_checks)
if derm_has_data and lesion_s and lesion_s > 5:
    output.append("[!] DERMATO: Multiple Skin Lesions detected. Further dermatological evaluation advised.")
ph_level = val("ph_level", derm_checks)
if derm_has_data and ph_level and (ph_level < 4.5 or ph_level > 8.5):
    output.append("[!] DERMATO: Abnormal Skin pH levels detected. Further dermatological evaluation advised.")
pruritus = derm_checks["pruritus"]
if derm_has_data and pruritus:
    output.append("[!] DERMATO: Pruritus reported. Possible dermatological evaluation recommended.")
erythema = derm_checks["erythema"]
if derm_has_data and erythema:
    output.append("[!] DERMATO: Erythema reported. Further dermatological assessment advised.")
vesicles = derm_checks["vesicles"]
if derm_has_data and vesicles:
    output.append("[!] DERMATO: Vesicular lesions observed. Possible infectious or inflammatory evaluation recommended.")
scaling = derm_checks["scaling"]
if derm_has_data and scaling:
    output.append("[!] DERMATO: Skin Scaling reported. Further dermatological evaluation advised.")
pigment = derm_checks["pigment"]
if derm_has_data and pigment:
    output.append("[!] DERMATO: Pigmentary changes observed. Possible dermatological disorder evaluation recommended.")
asym = derm_checks["asym"]
if derm_has_data and asym:
    output.append("[!] DERMATO: Asymmetrical skin lesions observed. Possible malignancy evaluation advised.")
u_healing = derm_checks["u_healing"]
if derm_has_data and u_healing:
    output.append("[!] DERMATO: Non-healing ulcers reported. Further dermatological assessment recommended.")
if psych_has_data:
    output.append("\n=== 🧠 PSYCHIATRIC ANALYSIS ===")
phq9 = val("phq9", psych_checks)
if psych_has_data and phq9 and phq9 >= 15:
    output.append("[ALERT] PSYCHIATRIC: Moderate to Severe Depression indicated by PHQ-9 score. Psychiatric evaluation advised.")
gad7 = val("gad7", psych_checks)
if psych_has_data and gad7 and gad7 >= 10:
    output.append("[ALERT] PSYCHIATRIC: Moderate to Severe Anxiety indicated by GAD-7 score. Further assessment recommended.")
sleep_h = val("sleep_h", psych_checks)
if psych_has_data and sleep_h and (sleep_h < 6 or sleep_h > 9):
    output.append("[!] PSYCHIATRIC: Abnormal Sleep Duration reported. Sleep hygiene evaluation advised.")
anhedonia = psych_checks["anhedonia"]
if psych_has_data and anhedonia:
    output.append("[!] PSYCHIATRIC: Anhedonia reported. Further psychiatric evaluation recommended.")
anxiety = psych_checks["anxiety"]
if psych_has_data and anxiety:
    output.append("[!] PSYCHIATRIC: Anxiety symptoms reported. Comprehensive psychiatric assessment advised.")
halluc = psych_checks["halluc"]
if psych_has_data and halluc:
    output.append("[!] PSYCHIATRIC: Hallucinations reported. Immediate psychiatric evaluation recommended.")
mania = psych_checks["mania"]
if psych_has_data and mania:
    output.append("[!] PSYCHIATRIC: Manic symptoms reported. Further psychiatric assessment advised.")
suicide = psych_checks["suicide"]
if psych_has_data and suicide:
    output.append("[!] PSYCHIATRIC: Suicidal ideation reported. Immediate psychiatric evaluation recommended.")
memory = psych_checks["memory"]
if psych_has_data and memory:
    output.append("[!] PSYCHIATRIC: Memory issues reported. Further psychiatric evaluation advised.")
if neph_has_data:
    output.append("\n=== 💧 NEPHROLOGY ANALYSIS ===")

creat_n = val("creat", neph_checks)
if neph_has_data and creat_n and creat_n > 1.5:
    output.append("[!] NEPHROLOGICAL: Elevated Serum Creatinine level detected. Possible renal dysfunction evaluation advised.")
egfr_n = val("egfr", neph_checks)
if neph_has_data and egfr_n and egfr_n < 60:
    output.append("[!] NEPHROLOGICAL: Reduced eGFR level detected. Possible chronic kidney disease evaluation advised.")
bun_n = val("bun", neph_checks)
if neph_has_data and bun_n and bun_n > 20:
    output.append("[!] NEPHROLOGICAL: Elevated BUN level detected. Possible renal dysfunction evaluation advised.")
k_level = val("k_level", neph_checks)
if neph_has_data and k_level and k_level > 5.5:
    output.append("[!] NEPHROLOGICAL: Elevated Potassium (K+) level detected. Possible hyperkalemia evaluation advised.")
u_alb = val("u_alb", neph_checks)
if neph_has_data and u_alb and u_alb > 300:
    output.append("[!] NEPHROLOGICAL: Elevated Albumin/Creatinine Ratio detected. Possible nephropathy evaluation advised.")
hematuria = neph_checks["hematuria"]
if neph_has_data and hematuria:
    output.append("[!] NEPHROLOGICAL: Hematuria reported. Further nephrological assessment recommended.")
foamy = neph_checks["foamy"]
if neph_has_data and foamy:
    output.append("[!] NEPHROLOGICAL: Foamy urine reported. Possible nephropathy evaluation advised.")
oliguria = neph_checks["oliguria"]
if neph_has_data and oliguria:
    output.append("[!] NEPHROLOGICAL: Oliguria reported. Further nephrological assessment recommended.")
u_edema = neph_checks["u_edema"]
if neph_has_data and u_edema:
    output.append("[!] NEPHROLOGICAL: Periorbital edema reported. Further nephrological assessment recommended.")
u_itch = neph_checks["u_itch"]
if neph_has_data and u_itch:
    output.append("[!] NEPHROLOGICAL: Uremic pruritus reported. Further nephrological assessment recommended.")
if hem_has_data:
    output.append("\n=== 🩸 HEMATOLOGICAL ANALYSIS ===")
hb = val("hb", hem_checks)
if hem_has_data and hb and hb < 12:
    output.append("[!] HEMATOLOGICAL: Low Hemoglobin level detected. Possible anemia evaluation recommended.")
wbc_h = val("wbc", hem_checks)
if hem_has_data and wbc_h and wbc_h < 4000:
    output.append("[!] HEMATOLOGICAL: Low WBC count detected. Possible immunodeficiency evaluation recommended.")
elif hem_has_data and wbc_h and wbc_h > 11000:
    output.append("[!] HEMATOLOGICAL: Elevated WBC count detected. Possible infection or inflammatory evaluation recommended.")
plt_h = val("plt", hem_checks)
if hem_has_data and plt_h and plt_h < 150000:
    output.append("[!] HEMATOLOGICAL: Low Platelet count detected. Possible bleeding disorder evaluation recommended.")
elif hem_has_data and plt_h and plt_h > 450000:
    output.append("[!] HEMATOLOGICAL: Elevated Platelet count detected. Possible thrombotic disorder evaluation recommended.")
mcv_h = val("mcv", hem_checks)
if hem_has_data and mcv_h and (mcv_h < 80 or mcv_h > 100):
    output.append("[!] HEMATOLOGICAL: Abnormal MCV level detected. Further hematological evaluation advised.")
inr_h = val("inr", hem_checks)
if hem_has_data and inr_h and (inr_h < 0.8 or inr_h > 1.2):
    output.append("[!] HEMATOLOGICAL: Abnormal INR level detected. Coagulation disorder evaluation recommended.")
ferritin = val("ferritin", hem_checks)
if hem_has_data and ferritin and (ferritin < 30 or ferritin > 400):
    output.append("[!] HEMATOLOGICAL: Abnormal Ferritin level detected. Possible iron metabolism disorder evaluation advised.")
pallor = hem_checks["pallor"]
if hem_has_data and pallor:
    output.append("[!] HEMATOLOGICAL: Pallor reported. Possible anemia evaluation recommended.")
petechiae_h = hem_checks["petechiae"]
if hem_has_data and petechiae_h:
    output.append("[!] HEMATOLOGICAL: Petechiae reported. Possible platelet disorder evaluation recommended.")
lymph_h = hem_checks["lymph"]
if hem_has_data and lymph_h:
    output.append("[!] HEMATOLOGICAL: Lymphadenopathy detected. Further infectious and oncologic workup recommended.")
spleno_h = hem_checks["spleno"]
if hem_has_data and spleno_h:
    output.append("[!] HEMATOLOGICAL: Splenomegaly detected. Further hematologic evaluation advised.")
epistax = hem_checks["epistax"]
if hem_has_data and epistax:
    output.append("[!] HEMATOLOGICAL: Epistaxis reported. Possible bleeding disorder evaluation recommended.")

if st.session_state.analysis_requested:
    if st.session_state.uploaded_images:
        output.extend(
            summarize_uploaded_files(
                st.session_state.uploaded_images,
                patient_name,
                patient_age,
                patient_gender,
            )
        )

    if len("\n".join(output).strip()) < 60:
        output.append("[+] ANALYSIS: No major anomalies detected. Patient appears to be in good health status.")
    st.session_state.analysis_output = "\n".join(output)
    
