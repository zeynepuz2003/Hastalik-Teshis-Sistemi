"""
Sayfa: Belirti Seçimi — belirti grupları, teşhis tetikleyici ve ajan log kaydı.
"""

import datetime
import streamlit as st

from engine.knowledge_base import SYMPTOM_GROUPS

from app_ui.theme      import palette
from app_ui.helpers    import t, sl, go
from app_ui.components import render_steps, render_patient_bar
from app_ui.diagnosis  import run_diagnosis


def page_symptoms():
    render_steps("symptoms")
    render_patient_bar()
    p = palette()

    st.markdown(f"""
    <div style="background:{p['surface']};border:1px solid {p['border']};
         border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;
         box-shadow:{p['shadow_sm']};">
      <div style="font-size:1.05rem;font-weight:700;color:{p['accent']};
           margin-bottom:.3rem;">🩺 {t('sym_title')}</div>
      <div style="font-size:.82rem;color:{p['muted']};">{t('sym_sub')}</div>
    </div>
    """, unsafe_allow_html=True)

    prev     = set(st.session_state.selected_symptoms)
    selected = set()

    for group, symptoms in SYMPTOM_GROUPS.items():
        st.markdown(f"""
        <div style="font-size:.75rem;font-weight:700;text-transform:uppercase;
             letter-spacing:.08em;color:{p['accent']};border-bottom:1px solid {p['border']};
             padding-bottom:.3rem;margin:.9rem 0 .5rem 0;">📂 {group}</div>
        """, unsafe_allow_html=True)
        cols = st.columns(3)
        for i, sym in enumerate(symptoms):
            with cols[i % 3]:
                if st.checkbox(sl(sym), value=(sym in prev), key=f"sym_{sym}"):
                    selected.add(sym)

    cnt = len(selected)
    st.markdown(f"""
    <div style="text-align:center;
         background:{'rgba(79,142,247,.1)' if st.session_state.dark else 'rgba(37,99,235,.07)'};
         border:1px solid {p['accent']};border-radius:8px;
         padding:.65rem;margin:1rem 0;font-size:.9rem;color:{p['accent']};">
      ✅ <b>{cnt}</b> {t('selected')}
    </div>
    """, unsafe_allow_html=True)

    c_back, c_diag = st.columns([1, 2])
    with c_back:
        if st.button(t("back"), use_container_width=True):
            st.session_state.selected_symptoms = list(selected)
            go("profile")

    with c_diag:
        if st.button(f"🔍  {t('diagnose')}", use_container_width=True, type="primary"):
            if cnt == 0:
                st.error(t("no_sym"))
            else:
                st.session_state.selected_symptoms = list(selected)
                with st.spinner("Analiz yapılıyor… / Analyzing…"):
                    st.session_state.results = run_diagnosis(list(selected))

                # ── Ajan izleme logu ──────────────────────────────────────
                res = st.session_state.results
                d0  = res["diagnoses"][0]
                st.session_state.monitor_log.append({
                    "ts":          datetime.datetime.now().strftime("%H:%M:%S"),
                    "n_sym":       cnt,
                    "top":         d0["name"],
                    "score":       d0["final"],
                    "bayes":       d0["bayes"],
                    "cosine":      d0["cosine"],
                    "logic_s":     d0["logic"],
                    "rules_fired": res["logic"]["fired_count"],
                    "opt_init":    res["optim"]["init"],
                    "opt_final":   res["optim"]["final"],
                    "opt_improve": res["optim"]["improve"],
                    "opt_iters":   res["optim"]["iters"],
                    "opt_conv":    res["optim"]["converged"],
                    "rule_ids":    [r["id"] for r in res["logic"]["rules"]],
                })
                go("results")
