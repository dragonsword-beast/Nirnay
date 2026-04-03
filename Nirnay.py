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

# ============================================
# MODERN SAAS WEBSITE DESIGN
# ============================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}
    .stDeployButton {display: none;}

    :root {
        /* Light theme colors */
        --primary-bg: #ffffff;
        --secondary-bg: #f8fafc;
        --surface-bg: #ffffff;
        --card-bg: #ffffff;
        --text-primary: #1a365d;
        --text-secondary: #4a5568;
        --text-muted: #718096;
        --border-color: #e2e8f0;
        --border-hover: #cbd5e0;
        --shadow: rgba(0, 0, 0, 0.1);
        --shadow-hover: rgba(0, 0, 0, 0.15);
        --navbar-bg: rgba(255, 255, 255, 0.95);
        --navbar-border: rgba(0, 0, 0, 0.1);
        --gradient-start: #667eea;
        --gradient-end: #764ba2;
        --accent-primary: #3b82f6;
        --accent-secondary: #06b6d4;
    }

    [data-theme="dark"] {
        /* Dark theme colors */
        --primary-bg: #0f172a;
        --secondary-bg: #1e293b;
        --surface-bg: #1e293b;
        --card-bg: rgba(30, 41, 59, 0.8);
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --text-muted: #94a3b8;
        --border-color: rgba(148, 163, 184, 0.2);
        --border-hover: rgba(148, 163, 184, 0.3);
        --shadow: rgba(0, 0, 0, 0.3);
        --shadow-hover: rgba(0, 0, 0, 0.4);
        --navbar-bg: rgba(15, 23, 42, 0.95);
        --navbar-border: rgba(148, 163, 184, 0.2);
        --gradient-start: #3b82f6;
        --gradient-end: #1e40af;
        --accent-primary: #60a5fa;
        --accent-secondary: #22d3ee;
    }

    * {
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
        background: var(--primary-bg);
        color: var(--text-primary);
        line-height: 1.6;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }

    /* ============================================
       NAVIGATION BAR
       ============================================ */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: var(--navbar-bg);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--navbar-border);
        padding: 0;
        transition: all 0.3s ease;
    }

    .navbar-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 70px;
    }

    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        text-decoration: none;
    }

    .navbar-logo {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.2rem;
    }

    .navbar-nav {
        display: flex;
        gap: 2rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .nav-link {
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }

    .nav-link:hover {
        color: var(--accent-primary);
    }

    /* ============================================
       HERO SECTION
       ============================================ */
    .hero-section {
        padding: 120px 2rem 80px;
        text-align: center;
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        color: white;
        margin-top: 70px;
    }

    .hero-container {
        max-width: 800px;
        margin: 0 auto;
    }

    .hero-title {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        margin-bottom: 1rem;
        line-height: 1.1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .hero-subtitle {
        font-size: clamp(1.1rem, 2.5vw, 1.3rem);
        font-weight: 400;
        margin-bottom: 2rem;
        opacity: 0.9;
        line-height: 1.6;
    }

    .hero-cta {
        display: inline-flex;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50px;
        color: white;
        text-decoration: none;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .hero-cta:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }

    /* ============================================
       FEATURES SECTION
       ============================================ */
    .features-section {
        padding: 80px 2rem;
        background: var(--secondary-bg);
    }

    .features-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .features-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .features-title {
        font-size: clamp(2rem, 4vw, 2.5rem);
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    .features-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
    }

    .feature-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px var(--shadow);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px var(--shadow-hover);
    }

    .feature-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 1rem;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }

    .feature-description {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ============================================
       MAIN TOOL SECTION
       ============================================ */
    .tool-section {
        padding: 80px 2rem;
        background: var(--primary-bg);
    }

    .tool-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .tool-header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .tool-title {
        font-size: clamp(2rem, 4vw, 2.5rem);
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    .tool-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        max-width: 600px;
        margin: 0 auto;
    }

    /* ============================================
       STEP-BY-STEP WORKFLOW
       ============================================ */
    .workflow-container {
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px var(--shadow);
    }

    .stepper {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stepper-step {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        padding: 1rem;
        border-radius: 12px;
        background: var(--secondary-bg);
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stepper-step.active {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        color: white;
        border-color: var(--gradient-start);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    .stepper-step.completed {
        background: var(--accent-primary);
        color: white;
        border-color: var(--accent-primary);
    }

    .stepper-step .status {
        font-size: 0.8rem;
        font-weight: bold;
    }

    /* ============================================
       FORM ELEMENTS
       ============================================ */
    .form-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px var(--shadow);
    }

    .form-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-align: center;
    }

    /* ============================================
       RESULTS SECTION
       ============================================ */
    .results-container {
        background: var(--surface-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px var(--shadow);
    }

    .results-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .results-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .results-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }

    .result-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px var(--shadow);
    }

    .result-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
    }

    .result-content {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ============================================
       CHAT INTERFACE
       ============================================ */
    .chat-section {
        padding: 80px 2rem;
        background: var(--secondary-bg);
    }

    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }

    .chat-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .chat-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    .chat-subtitle {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }

    .chat-messages {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 2rem 0;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: 0 4px 6px var(--shadow);
    }

    .message {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        align-items: flex-start;
    }

    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    .message.user .message-avatar {
        background: var(--accent-primary);
        color: white;
    }

    .message.assistant .message-avatar {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        color: white;
    }

    .message-content {
        flex: 1;
        background: var(--secondary-bg);
        border-radius: 12px;
        padding: 1rem;
        color: var(--text-primary);
        line-height: 1.6;
    }

    .chat-input-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }

    /* ============================================
       FOOTER
       ============================================ */
    .footer {
        background: var(--text-primary);
        color: white;
        padding: 3rem 2rem 2rem;
        margin-top: 4rem;
    }

    .footer-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }

    .footer-section h3 {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .footer-section p {
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.6;
    }

    .footer-links {
        display: flex;
        gap: 2rem;
        justify-content: center;
        margin-bottom: 1rem;
    }

    .footer-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        transition: color 0.3s ease;
    }

    .footer-link:hover {
        color: white;
    }

    .footer-bottom {
        text-align: center;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.6);
    }

    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    @media (max-width: 768px) {
        .navbar-container {
            padding: 0 1rem;
        }

        .navbar-nav {
            display: none;
        }

        .hero-section {
            padding: 100px 1rem 60px;
        }

        .hero-title {
            font-size: 2.5rem;
        }

        .features-section,
        .tool-section,
        .chat-section {
            padding: 60px 1rem;
        }

        .features-grid {
            grid-template-columns: 1fr;
        }

        .stepper {
            grid-template-columns: 1fr;
        }

        .workflow-container,
        .results-container {
            padding: 2rem 1rem;
        }

        .footer-content {
            grid-template-columns: 1fr;
            text-align: center;
        }

        .footer-links {
            flex-direction: column;
            gap: 1rem;
        }

        .chat-input-container {
            flex-direction: column;
        }

        .message {
            gap: 0.75rem;
        }

        .message-content {
            padding: 0.75rem;
        }
    }

    @media (max-width: 480px) {
        .hero-title {
            font-size: 2rem;
        }

        .workflow-container,
        .results-container {
            margin: 1rem 0;
            padding: 1.5rem 0.75rem;
        }

        .form-card {
            padding: 1.5rem 1rem;
        }

        .chat-messages {
            padding: 1rem;
        }
    }

    /* ============================================
       UTILITY CLASSES
       ============================================ */
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .text-center {
        text-align: center;
    }

    .mb-2 { margin-bottom: 1rem; }
    .mb-3 { margin-bottom: 1.5rem; }
    .mb-4 { margin-bottom: 2rem; }

    .mt-2 { margin-top: 1rem; }
    .mt-3 { margin-top: 1.5rem; }
    .mt-4 { margin-top: 2rem; }

    /* Hide Streamlit elements */
    .stApp > header {
        display: none;
    }

    .stApp > footer {
        display: none;
    }

    .stMain {
        margin-top: 0;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--secondary-bg);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-hover);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================
# MODERN SAAS WEBSITE CONTENT
# ============================================

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'chat_input' not in st.session_state:
    st.session_state.chat_input = ""

# ============================================
# NAVIGATION BAR
# ============================================
st.markdown(
    """
    <nav class="navbar">
        <div class="navbar-container">
            <a href="#" class="navbar-brand">
                <div class="navbar-logo">N</div>
                Nirnay
            </a>
            <ul class="navbar-nav">
                <li><a href="#features" class="nav-link">Features</a></li>
                <li><a href="#tool" class="nav-link">Tool</a></li>
                <li><a href="#chat" class="nav-link">AI Chat</a></li>
            </ul>
        </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

# ============================================
# HERO SECTION
# ============================================
st.markdown(
    """
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


def render_analysis_chat_styles():
    # Styles used in the Analysis + Chat pages. Add or extend custom CSS as needed.
    st.markdown(
        """
        <style>
        .dashboard-shell { margin-bottom: 20px; }
        .glass-card { border-radius: 12px; }
        .analysis-report-box { padding: 10px; }
        .assistant-panel { border: 1px solid #ddd; padding: 10px; }
        </style>
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
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


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
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def load_saved_profile():
    label = st.session_state.selected_saved_profile
    for p in st.session_state.saved_profiles:
        if f"{p['name']} · {p['age']} · {p['gender']}" == label:
            st.session_state.patient_name = p["name"]
            st.session_state.patient_age = p["age"]
            st.session_state.patient_gender = p["gender"]
            break
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def continue_to_analysis():
    set_page("analysis")


def reset_profile():
    st.session_state.patient_name = ""
    st.session_state.patient_age = ""
    st.session_state.patient_gender = ""
    st.session_state.agree_disclaimer = False
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def back_to_analysis():
    set_page("analysis")


def request_analysis():
    st.session_state.analysis_requested = True

def launch_chat(mode):
    st.session_state.chat_mode = mode
    st.session_state.page = "chat"

# ============================================
# MODERN SAAS WEBSITE CONTENT
# ============================================

# ============================================
# PROFILE PAGE (INTAKE FORM)
# ============================================
if page == "profile":
    # ============================================
    # NAVIGATION BAR
    # ============================================
    st.markdown(
        """
        <nav class="navbar">
            <div class="navbar-container">
                <a href="#" class="navbar-brand">
                    <div class="navbar-logo">N</div>
                    Nirnay
                </a>
                <ul class="navbar-nav">
                    <li><a href="#features" class="nav-link">Features</a></li>
                    <li><a href="#tool" class="nav-link">Tool</a></li>
                    <li><a href="#chat" class="nav-link">AI Chat</a></li>
                </ul>
            </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )

    # ============================================
    # HERO SECTION
    # ============================================
    st.markdown(
        """
        <section class="hero-section">
            <div class="hero-container">
                <h1 class="hero-title">AI-Powered Clinical Diagnostic Workflow</h1>
                <p class="hero-subtitle">
                    Transform your medical assessment process with intelligent automation, comprehensive analysis,
                    and real-time AI assistance for healthcare professionals.
                </p>
                <a href="#tool" class="hero-cta">Start Assessment →</a>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # ============================================
    # FEATURES SECTION
    # ============================================
    st.markdown(
        """
        <section class="features-section" id="features">
            <div class="features-container">
                <div class="features-header">
                    <h2 class="features-title">Why Choose Nirnay?</h2>
                    <p class="features-subtitle">
                        Advanced AI technology meets clinical excellence to streamline your diagnostic workflow.
                    </p>
                </div>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <h3 class="feature-title">AI-Powered Analysis</h3>
                        <p class="feature-description">
                            Leverage advanced machine learning algorithms for comprehensive symptom analysis and risk assessment.
                        </p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3 class="feature-title">Rapid Assessment</h3>
                        <p class="feature-description">
                            Complete patient evaluations in minutes with our streamlined, intuitive workflow interface.
                        </p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🤖</div>
                        <h3 class="feature-title">24/7 AI Assistant</h3>
                        <p class="feature-description">
                            Get instant answers to clinical questions and access evidence-based medical insights anytime.
                        </p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🔒</div>
                        <h3 class="feature-title">Secure & Private</h3>
                        <p class="feature-description">
                            Enterprise-grade security with HIPAA-compliant data handling and privacy protection.
                        </p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3 class="feature-title">Comprehensive Reports</h3>
                        <p class="feature-description">
                            Generate detailed clinical reports with differential diagnoses and treatment recommendations.
                        </p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📱</div>
                        <h3 class="feature-title">Mobile Optimized</h3>
                        <p class="feature-description">
                            Fully responsive design that works seamlessly across all devices and screen sizes.
                        </p>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # ============================================
    # TOOL SECTION (INTAKE FORM)
    # ============================================
    st.markdown(
        """
        <section class="tool-section" id="tool">
            <div class="tool-container">
                <div class="tool-header">
                    <h2 class="tool-title">Patient Intake Form</h2>
                    <p class="tool-subtitle">
                        Begin your clinical assessment by providing patient information and symptoms.
                    </p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.patient_name = st.text_input(
                "👤 Full name",
                value=st.session_state.patient_name,
                placeholder="e.g. Priya Sharma",
            )
        with col2:
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
        with col3:
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
            render_footer()
            st.stop()

        col1, col2 = st.columns([3, 2])
        with col1:
            st.button(
                "Begin Assessment",
                key="continue_to_analysis",
                on_click=continue_to_analysis,
                disabled=not valid_profile,
            )
        with col2:
            st.button(
                "Save profile",
                key="save_profile",
                on_click=save_profile,
                disabled=not profile_save_ready,
            )

        if st.session_state.profile_saved:
            st.success("Profile saved successfully. You can load it later from Saved profiles.")

        st.button("Reset profile", key="reset_profile", on_click=reset_profile)
        render_footer()
        st.stop()

# ============================================
# NAVIGATION BAR
# ============================================
st.markdown(
    """
    <nav class="navbar">
        <div class="navbar-container">
            <a href="#" class="navbar-brand">
                <div class="navbar-logo">N</div>
                Nirnay
            </a>
            <ul class="navbar-nav">
                <li><a href="#features" class="nav-link">Features</a></li>
                <li><a href="#tool" class="nav-link">Tool</a></li>
                <li><a href="#chat" class="nav-link">AI Chat</a></li>
            </ul>
        </div>
    </nav>
    """,
    unsafe_allow_html=True,
)

# ============================================
# HERO SECTION
# ============================================
st.markdown(
    """
    <section class="hero-section">
        <div class="hero-container">
            <h1 class="hero-title">AI-Powered Clinical Diagnostic Workflow</h1>
            <p class="hero-subtitle">
                Transform your medical assessment process with intelligent automation, comprehensive analysis,
                and real-time AI assistance for healthcare professionals.
            </p>
            <a href="#tool" class="hero-cta">Start Assessment →</a>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ============================================
# FEATURES SECTION
# ============================================
st.markdown(
    """
    <section class="features-section" id="features">
        <div class="features-container">
            <div class="features-header">
                <h2 class="features-title">Why Choose Nirnay?</h2>
                <p class="features-subtitle">
                    Advanced AI technology meets clinical excellence to streamline your diagnostic workflow.
                </p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h3 class="feature-title">AI-Powered Analysis</h3>
                    <p class="feature-description">
                        Leverage advanced machine learning algorithms for comprehensive symptom analysis and risk assessment.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3 class="feature-title">Rapid Assessment</h3>
                    <p class="feature-description">
                        Complete patient evaluations in minutes with our streamlined, intuitive workflow interface.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <h3 class="feature-title">24/7 AI Assistant</h3>
                    <p class="feature-description">
                        Get instant answers to clinical questions and access evidence-based medical insights anytime.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3 class="feature-title">Secure & Private</h3>
                    <p class="feature-description">
                        Enterprise-grade security with HIPAA-compliant data handling and privacy protection.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3 class="feature-title">Comprehensive Reports</h3>
                    <p class="feature-description">
                        Generate detailed clinical reports with differential diagnoses and treatment recommendations.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3 class="feature-title">Mobile Optimized</h3>
                    <p class="feature-description">
                        Fully responsive design that works seamlessly across all devices and screen sizes.
                    </p>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ============================================
# STEP-BY-STEP WORKFLOW
# ============================================

# Stepper Navigation
steps = ["Patient Intake", "Assessment", "Analysis", "Results"]
current_step = st.session_state.current_step

st.markdown('<div class="workflow-container">', unsafe_allow_html=True)

st.markdown('<div class="stepper">', unsafe_allow_html=True)

step_cols = st.columns(len(steps), gap="small")
for i, step in enumerate(steps):
    with step_cols[i]:
        if i < current_step:
            status = "completed"
            status_text = "✓"
        elif i == current_step:
            status = "active"
            status_text = str(i + 1)
        else:
            status = "upcoming"
            status_text = str(i + 1)

        st.markdown(
            f"""
            <div class="stepper-step {status}">
                <span class="status">{status_text}</span>
                {step}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# STEP 0: PATIENT INTAKE FORM
# ============================================
if current_step == 0:
    st.markdown(
        """
        <div class="form-card">
            <h2 class="form-title">Patient Information</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 2rem;">
                Please provide the patient's basic information to begin the assessment.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Patient Name", key="patient_name")
        age = st.number_input("Age", min_value=0, max_value=120, key="patient_age")
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"], key="patient_gender")

    with col2:
        symptoms = st.text_area("Chief Complaint/Symptoms", height=100, key="patient_symptoms")
        duration = st.text_input("Duration of Symptoms", placeholder="e.g., 3 days, 2 weeks", key="symptom_duration")

    # Next button
    if st.button("Begin Assessment →", key="next_step_0", use_container_width=True, type="primary"):
        if name and symptoms:
            st.session_state.patient_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "symptoms": symptoms,
                "duration": duration
            }
            st.session_state.current_step = 1
            st.rerun()

# ============================================
# STEP 1: ASSESSMENT
# ============================================
elif current_step == 1:
    patient = st.session_state.patient_data

    st.markdown(
        f"""
        <div class="form-card">
            <h2 class="form-title">Assessment: {patient.get('name', 'Patient')}</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 2rem;">
                Please provide additional assessment details for a comprehensive analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "Critical"], key="severity")
        pain_level = st.slider("Pain Level (1-10)", 1, 10, 5, key="pain_level")
        onset = st.selectbox("Onset", ["Sudden", "Gradual", "Unknown"], key="onset")

    with col2:
        associated_symptoms = st.text_area("Associated Symptoms", height=100, placeholder="e.g., fever, nausea, fatigue", key="associated_symptoms")
        medical_history = st.text_area("Relevant Medical History", height=100, placeholder="e.g., allergies, medications, past conditions", key="medical_history")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Intake", key="back_step_1"):
            st.session_state.current_step = 0
            st.rerun()

    with col2:
        if st.button("Generate Analysis →", key="next_step_1", use_container_width=True, type="primary"):
            st.session_state.patient_data.update({
                "severity": severity,
                "pain_level": pain_level,
                "onset": onset,
                "associated_symptoms": associated_symptoms,
                "medical_history": medical_history
            })
            st.session_state.current_step = 2
            st.session_state.is_processing = True
            st.rerun()

# ============================================
# STEP 2: ANALYSIS PROCESSING
# ============================================
elif current_step == 2:
    patient = st.session_state.patient_data

    st.markdown(
        """
        <div class="form-card">
            <h2 class="form-title">AI Analysis in Progress</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 2rem;">
                Our AI is analyzing the patient data and generating clinical recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()

    if st.session_state.is_processing:
        for i in range(101):
            progress_bar.progress(i)
            if i < 30:
                status_text.text("📊 Gathering patient information...")
            elif i < 60:
                status_text.text("🧠 Analyzing symptoms and medical history...")
            elif i < 90:
                status_text.text("⚡ Generating risk assessment...")
            else:
                status_text.text("✅ Finalizing clinical recommendations...")

            time.sleep(0.05)

        # Generate analysis
        patient_summary = f"""
        Patient: {patient.get('name', 'Unknown')}
        Age: {patient.get('age', 'Unknown')}
        Gender: {patient.get('gender', 'Unknown')}
        Symptoms: {patient.get('symptoms', 'None reported')}
        Duration: {patient.get('duration', 'Unknown')}
        Severity: {patient.get('severity', 'Unknown')}
        Pain Level: {patient.get('pain_level', 'Unknown')}
        Associated Symptoms: {patient.get('associated_symptoms', 'None reported')}
        Medical History: {patient.get('medical_history', 'None reported')}
        """

        analysis = run_groq_chat_sync(patient_summary)

        st.session_state.analysis_results = {
            "summary": patient_summary,
            "analysis": analysis,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        st.session_state.is_processing = False
        st.session_state.current_step = 3
        st.rerun()

    # Back button
    if st.button("← Back to Assessment", key="back_step_2"):
        st.session_state.current_step = 1
        st.rerun()

# ============================================
# STEP 3: RESULTS DISPLAY
# ============================================
elif current_step == 3:
    results = st.session_state.analysis_results
    patient = st.session_state.patient_data

    st.markdown(
        """
        <div class="results-container">
            <div class="results-header">
                <h2 class="results-title">📋 Clinical Assessment Results</h2>
                <p class="results-subtitle">Comprehensive analysis and recommendations for patient care</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Results grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="result-card">
                <div class="result-icon">👤</div>
                <h3 class="result-title">Patient Summary</h3>
                <div class="result-content">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Name:** {patient.get('name', 'N/A')}")
        st.markdown(f"**Age:** {patient.get('age', 'N/A')}")
        st.markdown(f"**Gender:** {patient.get('gender', 'N/A')}")
        st.markdown(f"**Symptoms:** {patient.get('symptoms', 'N/A')}")

        st.markdown('</div></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="result-card">
                <div class="result-icon">📊</div>
                <h3 class="result-title">Assessment Details</h3>
                <div class="result-content">
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"**Severity:** {patient.get('severity', 'N/A')}")
        st.markdown(f"**Pain Level:** {patient.get('pain_level', 'N/A')}/10")
        st.markdown(f"**Duration:** {patient.get('duration', 'N/A')}")
        st.markdown(f"**Onset:** {patient.get('onset', 'N/A')}")

        st.markdown('</div></div>', unsafe_allow_html=True)

    # AI Analysis
    st.markdown(
        """
        <div class="result-card">
            <div class="result-icon">🤖</div>
            <h3 class="result-title">AI Clinical Analysis</h3>
            <div class="result-content">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(results.get("analysis", "Analysis not available"))

    st.markdown('</div></div>', unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Back to Analysis", key="back_step_3"):
            st.session_state.current_step = 2
            st.rerun()

    with col2:
        if st.button("New Assessment", key="new_assessment"):
            # Reset everything
            st.session_state.current_step = 0
            st.session_state.patient_data = {}
            st.session_state.analysis_results = {}
            st.session_state.is_processing = False
            st.session_state.chat_messages = []
            st.rerun()

    with col3:
        if st.button("💬 AI Chat Assistant", key="open_chat", use_container_width=True, type="secondary"):
            pass  # Will scroll to chat section

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# AI CHAT ASSISTANT SECTION
# ============================================
st.markdown(
    """
    <section class="chat-section" id="chat">
        <div class="chat-container">
            <div class="chat-header">
                <h2 class="chat-title">🤖 AI Medical Assistant</h2>
                <p class="chat-subtitle">
                    Get instant answers to clinical questions and evidence-based medical insights.
                </p>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# Chat interface
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

# Display chat messages
if st.session_state.chat_messages:
    for message in st.session_state.chat_messages:
        message_class = "user" if message["role"] == "user" else "assistant"
        avatar = "👤" if message["role"] == "user" else "🤖"

        st.markdown(
            f"""
            <div class="message {message_class}">
                <div class="message-avatar">{avatar}</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        """
        <div class="message assistant">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                Hello! I'm your AI medical assistant. I can help you with:
                <br>• Clinical case analysis
                <br>• Symptom interpretation
                <br>• Medical literature insights
                <br>• Treatment considerations
                <br><br>
                <em>Please note: I'm not a substitute for professional medical advice.</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

col_input, col_send = st.columns([4, 1])

with col_input:
    user_input = st.text_area(
        "Ask a medical question...",
        key="chat_input",
        height=50,
        placeholder="e.g., What are the common causes of chest pain?",
        label_visibility="collapsed"
    )

with col_send:
    if st.button("Send", key="send_chat", use_container_width=True, type="primary"):
        if user_input.strip():
            # Add user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })

            # Get patient context if available
            patient_context = ""
            if st.session_state.patient_data:
                patient_context = f"Current patient: {st.session_state.patient_data.get('name', 'Unknown')}, Symptoms: {st.session_state.patient_data.get('symptoms', 'None')}"

            # Generate AI response
            ai_response = run_groq_chat_sync(f"{patient_context}\n\nUser: {user_input}")

            # Add AI message
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": ai_response
            })

            # Clear input
            st.session_state.chat_input = ""
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown(
    """
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Nirnay</h3>
                    <p>AI-powered clinical diagnostic workflow for modern healthcare professionals.</p>
                </div>
                <div class="footer-section">
                    <h3>Features</h3>
                    <p>Rapid patient assessment, risk stratification, and personalized clinical recommendations.</p>
                </div>
                <div class="footer-section">
                    <h3>Support</h3>
                    <p>Built for healthcare providers seeking efficient, accurate diagnostic support.</p>
                </div>
            </div>
            <div class="footer-links">
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Contact</a>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Nirnay. All rights reserved.</p>
            </div>
        </div>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.patient_name = st.text_input(
            "👤 Full name",
            value=st.session_state.patient_name,
            placeholder="e.g. Priya Sharma",
        )
    with col2:
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
    with col3:
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
        render_footer()
        st.stop()

    col1, col2 = st.columns([3, 2])
    with col1:
        st.button(
            "Begin Assessment",
            key="continue_to_analysis",
            on_click=continue_to_analysis,
            disabled=not valid_profile,
        )
    with col2:
        st.button(
            "Save profile",
            key="save_profile",
            on_click=save_profile,
            disabled=not profile_save_ready,
        )

    if st.session_state.profile_saved:
        st.success("Profile saved successfully. You can load it later from Saved profiles.")

    st.button("Reset profile", key="reset_profile", on_click=reset_profile)
    render_footer()
    st.stop()

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
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


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
            collected["🧪 Metabolism"],
            "Add glucose metrics, lipid markers, or classic diabetes symptoms such as thirst, polyuria, or slow wound healing.",
        ),
        (
            "❤️ Cardiac",
            collected["❤️ Cardiac"],
            "Add blood pressure, troponin, BNP, or chest pain/shortness of breath symptoms.",
        ),
        (
            "🧬 Oncology",
            collected["🧬 Oncology"],
            "Add mass size, weight loss, lymph node changes, tumor marker values, or new systemic symptoms.",
        ),
        (
            "🧠 Neurology",
            collected["🧠 Neurology"],
            "Add headaches, weakness, sensory changes, seizures, dizziness, or focal deficit details.",
        ),
        (
            "👩 Gynecology",
            collected["👩 Gynecology"],
            "Add menstrual changes, pelvic pain, discharge, infertility symptoms, or gynecologic exam findings.",
        ),
        (
            "🛡️ Immunology",
            collected["🛡️ Immunology"],
            "Add autoimmune markers, recurrent infection history, rashes, joint pain, or lymph node findings.",
        ),
        (
            "🦋 Endocrinology",
            collected["🦋 Endocrinology"],
            "Add thyroid labs, cortisol/PTH levels, metabolic symptoms, or hormone-related complaints.",
        ),
        (
            "👶 Pediatric",
            collected["👶 Pediatric"],
            "Add growth measures, developmental milestones, feeding issues, fever, or respiratory symptoms.",
        ),
        (
            "🧴 Dermatology",
            collected["🧴 Dermatology"],
            "Add rash description, lesion size, itching, scaling, or ulcer characteristics.",
        ),
        (
            "🧠 Psychiatry",
            collected["🧠 Psychiatry"],
            "Add mood, anxiety, sleep, cognitive impairment, or suicide risk details.",
        ),
        (
            "💧 Nephrology",
            collected["💧 Nephrology"],
            "Add kidney labs, urine changes, edema, blood in urine, or fluid balance concerns.",
        ),
        (
            "🩸 Hematology",
            collected["🩸 Hematology"],
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
    action_col, _ = st.columns([1, 2], gap="small")
    with action_col:
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

    st.markdown(
        f"<header><div class='avatar'>{'👩‍⚕️' if mode == 'medical' else '⚡'}</div><div><div class='chat-title'>{header}</div><div class='chat-subtitle'>{subtitle}</div></div></header>",
        unsafe_allow_html=True,
    )

    switch_col1, switch_col2 = st.columns([1, 1], gap="small")
    with switch_col1:
        st.button(
            "Medical Assistant",
            key="chat_mode_med_button",
            disabled=mode == "medical",
            on_click=launch_chat,
            args=("medical",),
        )
    with switch_col2:
        st.button(
            "Quick Assistant",
            key="chat_mode_quick_button",
            disabled=mode == "quick",
            on_click=launch_chat,
            args=("quick",),
        )

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
    suggestion_cols = st.columns(len(suggestion_texts), gap="small")
    for idx, suggestion in enumerate(suggestion_texts):
        suggestion_cols[idx].button(
            suggestion,
            key=f"chat_suggestion_{mode}_{idx}",
            on_click=fill_chat_prompt,
            args=(suggestion, input_key),
        )

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
    render_footer()
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
    ("🧪 Metabolism", vital_defs),
    ("❤️ Cardiac", cardiac_defs),
    ("🧬 Oncology", onco_defs),
    ("🧠 Neurology", neural_defs),
    ("👩 Gynecology", gynae_defs),
    ("🛡️ Immunology", immuno_defs),
    ("🦋 Endocrinology", endo_defs),
    ("👶 Pediatric", pedia_defs),
    ("🧴 Dermatology", derm_defs),
    ("🧠 Psychiatry", psych_defs),
    ("💧 Nephrology", neph_defs),
    ("🩸 Hematology", hema_defs),
]

if "analysis_requested" not in st.session_state:
    st.session_state.analysis_requested = False

try:
    expander_target = expander_placeholder
except NameError:
    expander_target = st.empty()

# ------------ Analysis page -------------
if page == "analysis":
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
                        <div class='metric-pill'><strong>{len(st.session_state.uploaded_images)} assets</strong><span><br>Uploaded files ready for review.</span></div>
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
        button_cols = st.columns(2, gap="large")
        with button_cols[0]:
            st.button("Open Insights Advisor", key="choose_medical_assistant", on_click=launch_chat, args=("medical",))
        with button_cols[1]:
            st.button("Open Quick Summary", key="choose_quick_assistant", on_click=launch_chat, args=("quick",))


    col1, col2 = st.columns([7, 3], gap="large")
    with col1:
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
            tabs_objs = st.tabs([x[0] for x in tab_names])
            collected = {}

            for (tab_title, defs), tab_obj in zip(tab_names, tabs_objs):
                with tab_obj:
                    collected[tab_title] = make_inputs(tab_obj, defs)

            any_section_data = any(
                any(value is not None and value is not False and value != "" for value in section.values())
                for section in [
                    collected["🧪 Metabolism"],
                    collected["❤️ Cardiac"],
                    collected["🧬 Oncology"],
                    collected["🧠 Neurology"],
                    collected["👩 Gynecology"],
                    collected["🛡️ Immunology"],
                    collected["🦋 Endocrinology"],
                    collected["👶 Pediatric"],
                    collected["🧴 Dermatology"],
                    collected["🧠 Psychiatry"],
                    collected["💧 Nephrology"],
                    collected["🩸 Hematology"],
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
            image_cols = st.columns(3)
            for idx, img in enumerate(st.session_state.uploaded_images):
                with image_cols[idx % 3]:
                    st.image(img, caption=img.name, width=300)
                    st.button(
                        "Remove",
                        key=f"remove_uploaded_image_{idx}",
                        on_click=remove_uploaded_image,
                        args=(idx,),
                    )

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

        st.markdown(
            "<div class='action-bar'><div class='action-copy'>Primary action will activate once at least one clinical input, manual symptom text, or image is provided.</div></div>",
            unsafe_allow_html=True,
        )
        action_cols = st.columns([4, 2, 2], gap="large")
        with action_cols[0]:
            st.button(
                "Run Analysis",
                key="generate_analysis",
                disabled=not any_section_data,
                on_click=request_analysis,
            )
        with action_cols[1]:
            st.button("Save Draft", key="save_draft")
        with action_cols[2]:
            st.button("Reset", key="reset_analysis")

        if st.session_state.get("analysis_output", "").strip():
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
            download_cols = st.columns([3, 1])
            with download_cols[1]:
                st.download_button(
                    "Download Report",
                    report_text,
                    file_name="nirnay_diagnostics_report.txt",
                    mime="text/plain",
                    key="download_report",
                )
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

    with col2:
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

v_checks = collected["🧪 Metabolism"]
c_checks = collected["❤️ Cardiac"]
o_checks = collected["🧬 Oncology"]
n_checks = collected["🧠 Neurology"]
g_checks = collected["👩 Gynecology"]
i_checks = collected["🛡️ Immunology"]
endo_checks = collected["🦋 Endocrinology"]
ped_checks = collected["👶 Pediatric"]
derm_checks = collected["🧴 Dermatology"]
psych_checks = collected["🧠 Psychiatry"]
neph_checks = collected["💧 Nephrology"]
hem_checks = collected["🩸 Hematology"]

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
    
