"""
Tema yönetimi: renk paleti ve global CSS enjeksiyonu.
"""

import streamlit as st


def palette() -> dict:
    """Aktif temaya (koyu/açık) göre renk sözlüğü döndürür."""
    if st.session_state.dark:
        return {
            "bg":        "#0d1117",
            "surface":   "#161b22",
            "surface2":  "#21262d",
            "border":    "#30363d",
            "text":      "#e6edf3",
            "muted":     "#8b949e",
            "accent":    "#4f8ef7",
            "accent2":   "#3d7de0",
            "success":   "#3fb950",
            "warning":   "#e3b341",
            "grad":      "linear-gradient(135deg,#4f8ef7,#7c3aed)",
            "shadow":    "0 4px 24px rgba(0,0,0,0.55)",
            "shadow_sm": "0 2px 8px rgba(0,0,0,0.4)",
        }
    return {
        "bg":        "#f0f4f8",
        "surface":   "#ffffff",
        "surface2":  "#e8edf2",
        "border":    "#d0d7de",
        "text":      "#1a202c",
        "muted":     "#6a737d",
        "accent":    "#2563eb",
        "accent2":   "#1d4ed8",
        "success":   "#16a34a",
        "warning":   "#d97706",
        "grad":      "linear-gradient(135deg,#2563eb,#7c3aed)",
        "shadow":    "0 4px 24px rgba(0,0,0,0.10)",
        "shadow_sm": "0 2px 8px rgba(0,0,0,0.07)",
    }


def inject_css():
    """Tüm uygulamaya global CSS stilini enjekte eder."""
    p = palette()
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {p['bg']} !important;
    font-family: 'Inter', sans-serif !important;
    color: {p['text']} !important;
}}
[data-testid="stSidebar"] {{ display:none !important; }}
#MainMenu, footer, header {{ visibility:hidden !important; }}

.block-container {{
    padding: 1.5rem 2rem 4rem 2rem !important;
    max-width: 1100px !important;
    margin: 0 auto !important;
}}

.stButton > button {{
    background: {p['accent']} !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.45rem 1.2rem !important;
    transition: all .2s !important;
    box-shadow: none !important;
}}
.stButton > button:hover {{
    background: {p['accent2']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(79,142,247,.35) !important;
}}
[data-testid="stFormSubmitButton"] > button[kind="secondary"],
.stButton > button[kind="secondary"] {{
    background: {p['surface2']} !important;
    color: {p['text']} !important;
    border: 1px solid {p['border']} !important;
}}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: {p['surface2']} !important;
    border: 1px solid {p['border']} !important;
    color: {p['text']} !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}}
.stSelectbox > div > div {{
    background: {p['surface2']} !important;
    border: 1px solid {p['border']} !important;
    border-radius: 8px !important;
    color: {p['text']} !important;
}}
label, .stCheckbox label, .stRadio label {{
    color: {p['text']} !important;
    font-family: 'Inter', sans-serif !important;
}}

.stSlider [data-baseweb="slider"] {{ padding: 0 !important; }}

.stTabs [data-baseweb="tab-list"] {{
    background: {p['surface2']} !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 3px !important;
    border: 1px solid {p['border']} !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: {p['muted']} !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}}
.stTabs [aria-selected="true"] {{
    background: {p['accent']} !important;
    color: #fff !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

.streamlit-expanderHeader {{
    background: {p['surface2']} !important;
    border-radius: 8px !important;
    border: 1px solid {p['border']} !important;
    color: {p['text']} !important;
    font-family: 'Inter', sans-serif !important;
}}
.streamlit-expanderContent {{
    background: {p['surface']} !important;
    border: 1px solid {p['border']} !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 1rem !important;
}}

::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{p['bg']}; }}
::-webkit-scrollbar-thumb {{ background:{p['border']}; border-radius:3px; }}
.stAlert {{ border-radius:8px !important; }}
</style>
""", unsafe_allow_html=True)
