"""
Hastalık Teşhis Uzman Sistemi — Giriş Noktası
Tüm UI mantığı app_ui/ paketinde bulunur.
"""

import streamlit as st

from app_ui.helpers         import _init
from app_ui.theme           import inject_css
from app_ui.components      import render_banner
from app_ui.page_welcome    import page_welcome
from app_ui.page_profile    import page_profile
from app_ui.page_symptoms   import page_symptoms
from app_ui.page_results    import page_results
from app_ui.page_history    import page_history
from app_ui.page_monitoring import page_monitoring

st.set_page_config(
    page_title="DiagnosisAI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_init()
inject_css()
render_banner()

PAGES = {
    "welcome":    page_welcome,
    "profile":    page_profile,
    "symptoms":   page_symptoms,
    "results":    page_results,
    "history":    page_history,
    "monitoring": page_monitoring,
}

PAGES.get(st.session_state.page, page_welcome)()
