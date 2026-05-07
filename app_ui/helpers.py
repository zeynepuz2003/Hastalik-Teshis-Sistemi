"""
Yardımcı fonksiyonlar: session state, çeviri, navigasyon.
"""

import streamlit as st

from app_ui.translations import T, DISEASE_EN, SYM_EN
from engine.knowledge_base import SYMPTOM_LABELS


def _init():
    """Session state varsayılanlarını bir kez kurar."""
    defaults = {
        "page": "welcome", "lang": "TR", "dark": True,
        "role": None, "profile": {}, "selected_symptoms": [],
        "results": None, "history": [], "monitor_log": [],
        "eval_results": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def t(key: str) -> str:
    """Aktif dile göre çeviri döndürür."""
    return T[st.session_state.lang].get(key, key)


def dn(name: str) -> str:
    """Hastalık adını aktif dile çevirir."""
    if st.session_state.lang == "EN":
        return DISEASE_EN.get(name, name)
    return name


def sl(key: str) -> str:
    """Belirti anahtarını aktif dile çevirir."""
    if st.session_state.lang == "EN":
        return SYM_EN.get(key, SYMPTOM_LABELS.get(key, key))
    return SYMPTOM_LABELS.get(key, key)


def go(page: str):
    """Belirtilen sayfaya yönlendirir ve yeniden çizer."""
    st.session_state.page = page
    st.rerun()
