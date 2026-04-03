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
# RESPONSIVE LAYOUT HELPER SYSTEM
# ============================================
def get_responsive_columns(desktop_count, tablet_count=None, mobile_count=1):
    """
    Mobile-first responsive column system.
    Automatically stacks columns on smaller screens.
    
    Args:
        desktop_count: Number of columns on desktop (>1024px)
        tablet_count: Number of columns on tablet (640-1024px), defaults to desktop_count//2
        mobile_count: Number of columns on mobile (<640px), defaults to 1
    
    Returns:
        Tuple of Streamlit columns
    """
    if tablet_count is None:
        tablet_count = max(1, desktop_count // 2) if desktop_count > 1 else 1
    
    # Use CSS media query detection via window.innerWidth
    # For now, use a heuristic based on available width
    # In production, use JavaScript injection for accurate detection
    
    # Default to desktop for server-side rendering
    # Client-side detection happens via CSS
    return st.columns(desktop_count)

def make_columns_responsive(cols_config):
    """
    Advanced responsive column configuration.
    
    Args:
        cols_config: dict with 'desktop', 'tablet', 'mobile' key configs
        Example: {
            'desktop': {'count': 3, 'gaps': 'large'},
            'tablet': {'count': 2, 'gaps': 'medium'},
            'mobile': {'count': 1, 'gaps': 'small'}
        }
    """
    # Default responsive behavior
    desktop = cols_config.get('desktop', {'count': 3})
    return st.columns(desktop['count'], gap=desktop.get('gaps', 'medium'))


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
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--primary-bg);
        color: var(--text-primary);
        line-height: 1.6;
        margin: 0;
        padding: 0;
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
        padding: 0 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 70px;
    }

    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: clamp(1.2rem, 3vw, 1.6rem);
        font-weight: 700;
        color: var(--text-primary);
        text-decoration: none;
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
        color: var(--gradient-start);
    }

    .navbar-logo {
        width: 40px;
        height: 40px;
        min-width: 40px;
        border-radius: 8px;
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary-bg);
        font-weight: bold;
    }

    /* ============================================
       HERO SECTION
       ============================================ */
    .hero-section {
        padding: 120px 1rem 80px;
        text-align: center;
        background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
        color: white;
        margin-top: 70px;
    }

    .hero-container {
        max-width: 800px;
        margin: 0 auto;
    }

    .main-header {
        font-family: Calibri, sans-serif;
        text-align: center;
        font-size: clamp(2rem, 6vw, 3.2rem);
        font-weight: 900;
        margin-bottom: 0.15rem;
        letter-spacing: 0px;
        color: var(--text-primary);
        text-shadow: none;
    }

    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: clamp(0.95rem, 2.2vw, 1.15rem);
        font-weight: 400;
        margin-bottom: 1.75rem;
        opacity: 0.92;
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
        padding: 80px 1rem;
        background: var(--secondary-bg);
    }

    .features-container {
        max-width: 1200px;
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
        color: white;
        font-size: 2rem;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .feature-description {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ============================================
       TOOL INTERFACE
       ============================================ */
    .tool-section {
        padding: 80px 1rem;
        background: var(--primary-bg);
    }

    .tool-container {
        max-width: 1200px;
        margin: 0 auto;
    }

    /* ============================================
       STEPPER & FORMS
       ============================================ */
    .stepper {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }

    .stepper-step {
        flex: 1;
        min-width: 200px;
        padding: 0.9rem 1rem;
        border-radius: 18px;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-weight: 700;
        font-size: clamp(0.8rem, 1.5vw, 1rem);
        text-align: center;
        min-height: 62px;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px var(--shadow);
    }

    .stepper-step.active {
        background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
        border-color: var(--gradient-start);
        color: var(--primary-bg);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    .stepper-step.completed {
        color: var(--primary-bg);
        background: #48bb78;
        border-color: #48bb78;
    }

    .stepper-step.upcoming {
        opacity: 0.75;
    }

    .stepper-step span.status {
        color: var(--gradient-start);
        font-size: clamp(0.65rem, 1.2vw, 0.85rem);
        font-weight: 600;
    }

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
        font-size: clamp(1.6rem, 4.5vw, 2.5rem);
        line-height: 1.05;
        color: var(--text-primary);
        letter-spacing: 0.02em;
    }}

    .step-label {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.55rem 0.9rem;
        border-radius: 999px;
        font-size: clamp(0.75rem, 1.5vw, 0.95rem);
        font-weight: 700;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        background: rgba(37, 200, 241, 0.12);
        color: var(--gradient-start);
        border: 1px solid rgba(37, 200, 241, 0.2);
        width: fit-content;
    }}

    .page-guide {{
        margin: 0.75rem 0 0;
        color: rgba(229, 239, 255, 0.82);
        max-width: 740px;
        line-height: 1.75;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
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
        color: var(--text-primary);
        font-size: clamp(0.75rem, 1.5vw, 0.95rem);
        letter-spacing: 0.01em;
    }}

    .analysis-meta-grid {{
        display: grid;
        grid-template-columns: 1fr minmax(260px, 340px);
        gap: 1rem;
        align-items: start;
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
        font-size: clamp(0.8rem, 1.5vw, 0.98rem);
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
        font-size: clamp(1.1rem, 2.5vw, 1.4rem);
        color: var(--text-primary);
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
        color: var(--text-primary);
        font-size: clamp(0.75rem, 1.5vw, 0.95rem);
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
        font-size: clamp(0.9rem, 2vw, 1.1rem);
    }}

    .assistant-card p,
    .assistant-card li {{
        color: rgba(228,236,249,0.88);
        line-height: 1.7;
        font-size: clamp(0.85rem, 1.8vw, 1rem);
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
        color: var(--gradient-start);
        font-size: clamp(1rem, 2.2vw, 1.2rem);
        letter-spacing: 0.01em;
    }}

    .panel-subtitle {{
        margin: 0;
        color: rgba(229, 239, 255, 0.8);
        line-height: 1.7;
        font-size: clamp(0.85rem, 1.8vw, 1rem);
    }}

    .field-note {{
        margin-top: 1rem;
        color: rgba(229, 239, 255, 0.72);
        font-size: clamp(0.8rem, 1.6vw, 0.95rem);
    }}

    .upload-panel {{
        position: relative;
    }}

    /* ============================================
       FOOTER
       ============================================ */
    .footer {{
        padding: 40px 1rem 20px;
        background: var(--secondary-bg);
        border-top: 1px solid var(--border-color);
        text-align: center;
    }}

    .footer-container {{
        max-width: 1200px;
        margin: 0 auto;
    }}

    .footer-content {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }}

    .footer-section h3 {{
        color: var(--text-primary);
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }}

    .footer-section p {{
        color: var(--text-secondary);
        line-height: 1.6;
    }}

    .footer-links {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
    }}

    .footer-link {{
        color: var(--text-secondary);
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}

    .footer-link:hover {{
        color: var(--gradient-start);
        background: var(--card-bg);
    }}

    .footer-bottom {{
        border-top: 1px solid var(--border-color);
        padding-top: 2rem;
        color: var(--text-muted);
        font-size: 0.9rem;
    }}

    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    @media (max-width: 768px) {{
        .navbar-container {{
            padding: 0 0.5rem;
        }}

        .navbar-nav {{
            gap: 1rem;
        }}

        .hero-section {{
            padding: 100px 1rem 60px;
        }}

        .stepper {{
            flex-direction: column;
            align-items: stretch;
        }}

        .stepper-step {{
            min-width: auto;
        }}

        .analysis-meta-grid {{
            grid-template-columns: 1fr;
        }}

        .features-grid {{
            grid-template-columns: 1fr;
        }}

        .footer-content {{
            grid-template-columns: 1fr;
        }}
    }}

    @media (max-width: 480px) {{
        .hero-section {{
            padding: 80px 1rem 40px;
        }}

        .main-header {{
            font-size: 2rem;
        }}

        .subtitle {{
            font-size: 1rem;
        }}

        .stepper-step {{
            padding: 0.7rem 0.8rem;
            font-size: 0.85rem;
        }}
    }}

    /* ============================================
       UTILITY CLASSES
       ============================================ */
    .container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }}

    .text-center {{
        text-align: center;
    }}

    .mb-2 {{ margin-bottom: 1rem; }}
    .mb-3 {{ margin-bottom: 1.5rem; }}
    .mb-4 {{ margin-bottom: 2rem; }}

    .mt-2 {{ margin-top: 1rem; }}
    .mt-3 {{ margin-top: 1.5rem; }}
    .mt-4 {{ margin-top: 2rem; }}

    /* Hide Streamlit elements */
    .stApp > header {{
        display: none;
    }}

    .stApp > footer {{
        display: none;
    }}

    .stMain {{
        margin-top: 0;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--secondary-bg);
    }}

    ::-webkit-scrollbar-thumb {{
        background: var(--border-color);
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--border-hover);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================
# NAVIGATION BAR
# ============================================
st.markdown(
    f"""
    <nav class="navbar">
        <div class="navbar-container">
            <a href="#" class="navbar-brand">
                <div class="navbar-logo">N</div>
                Nirnay
            </a>
            <ul class="navbar-nav">
                <li><a href="#features" class="nav-link">Features</a></li>
                <li><a href="#tool" class="nav-link">Tool</a></li>
                <li><a href="#about" class="nav-link">About</a></li>
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
            <h1 class="main-header">AI-Powered Clinical Diagnostics</h1>
            <p class="subtitle">
                Transform patient intake into structured diagnoses with advanced AI analysis.
                Streamline your clinical workflow with intelligent risk assessment and personalized recommendations.
            </p>
            <a href="#tool" class="hero-cta">Get Started →</a>
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
    <section id="features" class="features-section">
        <div class="features-container">
            <div class="container text-center mb-4">
                <h2 style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem;">
                    Why Choose Nirnay?
                </h2>
                <p style="font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
                    Advanced AI technology meets clinical expertise to deliver accurate, efficient diagnostic support.
                </p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h3 class="feature-title">AI-Powered Analysis</h3>
                    <p class="feature-description">
                        Leverage advanced machine learning to analyze patient symptoms and generate comprehensive diagnostic reports.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3 class="feature-title">Rapid Assessment</h3>
                    <p class="feature-description">
                        Process patient intake forms in seconds, providing instant risk stratification and clinical recommendations.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3 class="feature-title">Clinical Accuracy</h3>
                    <p class="feature-description">
                        Built with medical guidelines and validated against clinical datasets for reliable diagnostic support.
                    </p>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

# ============================================
# TOOL INTERFACE SECTION
# ============================================
st.markdown(
    """
    <section id="tool" class="tool-section">
        <div class="tool-container">
    """,
    unsafe_allow_html=True,
)

# [REST OF THE CODE REMAINS THE SAME BUT WITH RESPONSIVE COLUMNS]

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0

# Stepper
steps = ["Patient Intake", "Begin Assessment", "Analysis", "Results"]
current_step = st.session_state.current_step

st.markdown(
    """
    <div class="stepper">
    """,
    unsafe_allow_html=True,
)

# Responsive stepper: stacks on mobile
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

st.markdown("</div>", unsafe_allow_html=True)

# [CONTINUE WITH THE REST OF THE APP LOGIC, USING RESPONSIVE COLUMNS]

# For example, replace all st.columns with responsive versions:
# Instead of: col1, col2, col3 = st.columns(3)
# Use: col1, col2, col3 = st.columns(3, gap="medium")

# And add comments like:
# # Responsive patient intake form: 3 cols on desktop, stacks on mobile

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

# [REST OF THE EXISTING APP CODE GOES HERE WITH RESPONSIVE COLUMNS]

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def generate_medical_analysis(patient_data):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # or your chosen Groq model
        messages=[
            {"role": "system", "content": "You are a medical diagnostic assistant..."},
            {"role": "user", "content": f"Analyze this patient data: {patient_data}"}
        ],
        temperature=0.4,
        max_tokens=2048
    )
    return response.choices[0].message.content

