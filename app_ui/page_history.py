"""
Sayfa: Teşhis Geçmişi — kaydedilmiş teşhislerin listesi.
"""

import streamlit as st

from app_ui.theme   import palette
from app_ui.helpers import t, go


def page_history():
    p    = palette()
    hist = st.session_state.history

    st.markdown(f"""
    <div style="background:{p['surface']};border:1px solid {p['border']};
         border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
         box-shadow:{p['shadow_sm']};">
      <div style="font-size:1.05rem;font-weight:700;color:{p['accent']};">
        📋 {t('hist_title')}
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not hist:
        st.info(t("hist_empty"))
    else:
        for entry in reversed(hist):
            st.markdown(f"""
            <div style="background:{p['surface']};border:1px solid {p['border']};
                 border-radius:10px;padding:.9rem 1.2rem;margin-bottom:.7rem;
                 display:flex;justify-content:space-between;align-items:center;
                 box-shadow:{p['shadow_sm']};">
              <div>
                <div style="font-size:1rem;font-weight:600;color:{p['accent']};">
                  {entry['top']}</div>
                <div style="font-size:.77rem;color:{p['muted']};margin-top:3px;">
                  👤 {entry['patient']} &nbsp;|&nbsp;
                  🕒 {entry['date']} &nbsp;|&nbsp;
                  🩺 {entry['sym_cnt']} belirti
                </div>
              </div>
              <div style="font-size:1.6rem;font-weight:800;color:{p['accent']};">
                {entry['score']}%</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button(f"🗑️  {t('hist_clear')}", use_container_width=False):
            st.session_state.history = []
            st.rerun()

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    if st.button(f"← {t('back')}", key="hist_back"):
        go("results" if st.session_state.results else "welcome")
