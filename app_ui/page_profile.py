"""
Sayfa: Kişisel Bilgiler — kullanıcı profil formu.
"""

import streamlit as st

from app_ui.theme      import palette
from app_ui.helpers    import t, go
from app_ui.components import render_steps


def page_profile():
    render_steps("profile")
    p    = palette()
    prof = st.session_state.profile

    st.markdown(f"""
    <div style="background:{p['surface']};border:1px solid {p['border']};
         border-radius:12px;padding:1.3rem 1.5rem;margin-bottom:1.2rem;
         box-shadow:{p['shadow_sm']};">
      <div style="font-size:1.05rem;font-weight:700;color:{p['accent']};
           margin-bottom:.3rem;">👤 {t('profile_title')}</div>
      <div style="font-size:.82rem;color:{p['muted']};">{t('profile_sub')}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            name       = st.text_input(t("name"), value=prof.get("name", ""))
            age_v      = st.number_input(t("age"), 1, 120, int(prof.get("age", 30)), step=1)
            blood_opts = ["A+","A−","B+","B−","AB+","AB−","0+","0−","Bilinmiyor/Unknown"]
            blood_idx  = (blood_opts.index(prof.get("blood","Bilinmiyor/Unknown"))
                          if prof.get("blood") in blood_opts else len(blood_opts) - 1)
            blood      = st.selectbox(t("blood"), blood_opts, index=blood_idx)
        with c2:
            surname  = st.text_input(t("surname"), value=prof.get("surname", ""))
            g_opts   = [t("gender_m"), t("gender_f"), t("gender_o")]
            g_idx    = g_opts.index(prof.get("gender", g_opts[0])) if prof.get("gender") in g_opts else 0
            gender   = st.selectbox(t("gender"), g_opts, index=g_idx)
            d_opts   = [t("dur_1"), t("dur_3"), t("dur_7"), t("dur_14")]
            d_idx    = d_opts.index(prof.get("duration", d_opts[0])) if prof.get("duration") in d_opts else 0
            duration = st.selectbox(t("duration"), d_opts, index=d_idx)

        pain_v = st.slider(t("pain"), 0, 10, int(prof.get("pain_val", 0)))
        ch, al = st.columns(2)
        with ch:
            chronic   = st.text_area(t("chronic"),   value=prof.get("chronic", ""),   height=68)
        with al:
            allergies = st.text_area(t("allergies"), value=prof.get("allergies", ""), height=68)

        cb, cn = st.columns(2)
        with cb:
            back_btn = st.form_submit_button(t("back"), use_container_width=True)
        with cn:
            next_btn = st.form_submit_button(t("next"), use_container_width=True, type="primary")

    if next_btn:
        if not name.strip() or not surname.strip():
            st.warning("Ad ve soyad zorunludur. / Name and surname are required.")
        else:
            st.session_state.profile = {
                "name": name.strip(), "surname": surname.strip(),
                "age": age_v, "gender": gender, "blood": blood,
                "duration": duration, "pain_val": pain_v,
                "chronic": chronic, "allergies": allergies,
            }
            go("symptoms")
    if back_btn:
        go("welcome")
