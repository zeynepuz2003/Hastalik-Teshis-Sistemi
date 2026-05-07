"""
Sayfa: Teşhis Sonuçları — 4 sekme: tüm teşhisler, matematik, optimizasyon, mantık.
"""

import datetime
import streamlit as st

from app_ui.theme      import palette
from app_ui.helpers    import t, dn, sl, go
from app_ui.components import render_steps, render_patient_bar, score_bar


def page_results():
    if not st.session_state.results:
        go("symptoms")
        return

    render_steps("results")
    render_patient_bar()

    p    = palette()
    res  = st.session_state.results
    diag = res["diagnoses"]
    top  = diag[0]

    # ── En iyi teşhis banner ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{p['grad']};border-radius:16px;padding:2rem;
         text-align:center;color:#fff;margin-bottom:1.4rem;
         box-shadow:0 8px 32px rgba(79,142,247,.35);">
      <div style="font-size:.85rem;opacity:.85;margin-bottom:.3rem;">🏆 {t('top_diag')}</div>
      <div style="font-size:1.9rem;font-weight:800;margin:.3rem 0;">{dn(top['name'])}</div>
      <div style="font-size:3.2rem;font-weight:900;line-height:1.1;">{top['final']}%</div>
      <div style="font-size:.82rem;opacity:.8;">{t('confidence')}</div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([
        f"📊 {t('all_diag')}",
        f"🔬 {t('math')}",
        f"⚙️ {t('optim')}",
        f"🧠 {t('logic')}",
    ])

    # ── Tab 1: Tüm teşhisler ─────────────────────────────────────────────
    with tabs[0]:
        for d in diag:
            rank_bg = (p["accent"] if d["rank"] == 1 else
                       (p["muted"] if d["rank"] == 2 else p["warning"]))
            st.markdown(f"""
            <div style="background:{p['surface']};border:1px solid {p['border']};
                 border-radius:11px;padding:1rem 1.2rem;margin-bottom:.7rem;
                 display:flex;align-items:center;gap:1rem;">
              <div style="width:36px;height:36px;border-radius:50%;
                   background:{rank_bg};color:#fff;display:flex;
                   align-items:center;justify-content:center;
                   font-weight:700;font-size:.9rem;flex-shrink:0;">#{d['rank']}</div>
              <div style="flex:1;">
                <div style="font-weight:600;font-size:1rem;color:{p['text']};">{dn(d['name'])}</div>
                <div style="font-size:.78rem;color:{p['muted']};margin-top:2px;">
                  {d['description'][:90]}…</div>
              </div>
              <div style="font-size:1.5rem;font-weight:800;color:{p['accent']};flex-shrink:0;">
                {d['final']}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        show_n = 8 if st.session_state.role == "doctor" else 3
        for d in diag[:show_n]:
            with st.expander(f"#{d['rank']} {dn(d['name'])} — {d['final']}%"):
                st.markdown(
                    score_bar(t("hybrid"),  d["final"],  p["accent"]) +
                    score_bar(t("bayes"),   d["bayes"],  p["success"]) +
                    score_bar(t("cosine"),  d["cosine"], "#a78bfa") +
                    score_bar(t("logic_s"), d["logic"],  p["warning"]),
                    unsafe_allow_html=True,
                )
                if d["matched"]:
                    badges = "".join(
                        f'<span style="display:inline-block;padding:3px 9px;border-radius:12px;'
                        f'font-size:.74rem;margin:2px;background:rgba(63,185,80,.12);'
                        f'color:{p["success"]};border:1px solid {p["success"]};">{sl(s)}</span>'
                        for s in d["matched"]
                    )
                    st.markdown(f"**{t('matched')}:** {badges}", unsafe_allow_html=True)
                if d["fired"]:
                    rules = "".join(
                        f'<span style="display:inline-block;padding:3px 9px;border-radius:12px;'
                        f'font-size:.74rem;margin:2px;background:rgba(79,142,247,.12);'
                        f'color:{p["accent"]};border:1px solid {p["accent"]};">'
                        f'[{r["id"]}] {r["name"]} ({r["confidence"]*100:.0f}%)</span>'
                        for r in d["fired"]
                    )
                    st.markdown(f"**{t('rules')}:** {rules}", unsafe_allow_html=True)

    # ── Tab 2: Matematik ─────────────────────────────────────────────────
    with tabs[1]:
        m = res["math"]
        for col, val, lbl in zip(
            st.columns(4),
            [m["mat_norm"], m["vec_norm"], m["n_sym"], m["eigenvals"][0]],
            [t("mat_norm"), t("vec_norm"), "# " + t("sym_title"), "λ₁"],
        ):
            with col:
                st.markdown(f"""
                <div style="background:{p['surface2']};border:1px solid {p['border']};
                     border-radius:9px;padding:.7rem;text-align:center;margin-bottom:.6rem;">
                  <div style="font-size:1.3rem;font-weight:700;color:{p['accent']};">{val}</div>
                  <div style="font-size:.68rem;color:{p['muted']};margin-top:2px;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)
        ev, var = m["eigenvals"], m["variance"]
        st.markdown(f"**{t('eigenvals')}:** `{ev[0]}` · `{ev[1]}` · `{ev[2]}`")
        st.markdown(
            score_bar(f"PC-1 ({var[0]}%)", var[0], p["accent"]) +
            score_bar(f"PC-2 ({var[1]}%)", var[1], "#a78bfa") +
            score_bar(f"PC-3 ({var[2]}%)", var[2], p["success"]),
            unsafe_allow_html=True,
        )

    # ── Tab 3: Optimizasyon ──────────────────────────────────────────────
    with tabs[2]:
        opt = res["optim"]
        for col, val, lbl in zip(
            st.columns(4),
            [f"{opt['init']}%", f"{opt['final']}%",
             f"+{opt['improve']}%", t("yes") if opt["converged"] else t("no")],
            [t("init_s"), t("final_s"), t("improve"), t("converged")],
        ):
            with col:
                st.markdown(f"""
                <div style="background:{p['surface2']};border:1px solid {p['border']};
                     border-radius:9px;padding:.7rem;text-align:center;margin-bottom:.6rem;">
                  <div style="font-size:1.25rem;font-weight:700;color:{p['accent']};">{val}</div>
                  <div style="font-size:.68rem;color:{p['muted']};margin-top:2px;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)
        st.line_chart(opt["history"], height=190, use_container_width=True)
        if opt["weights"]:
            st.markdown(f"**{t('weights')}**")
            for sym_lbl, w in sorted(opt["weights"].items(), key=lambda x: x[1], reverse=True):
                st.markdown(score_bar(f"{sym_lbl}  ({w})", min((w/3)*100,100), p["accent"]),
                            unsafe_allow_html=True)

    # ── Tab 4: Mantık ────────────────────────────────────────────────────
    with tabs[3]:
        lg = res["logic"]
        st.markdown(f"**{t('fired')}:** {lg['fired_count']}")
        for rule in lg["rules"]:
            conds = " ∧ ".join(sl(c) for c in rule["conditions"])
            st.markdown(f"""
            <div style="background:{p['surface']};border:1px solid {p['border']};
                 border-radius:10px;padding:1rem 1.2rem;margin-bottom:.6rem;">
              <div style="font-size:.9rem;font-weight:600;color:{p['text']};margin-bottom:.4rem;">
                [{rule['id']}] {rule['name']}
                <span style="display:inline-block;padding:2px 8px;border-radius:10px;
                     font-size:.72rem;background:rgba(79,142,247,.15);
                     color:{p['accent']};border:1px solid {p['accent']};margin-left:6px;">
                  {rule['confidence']}%</span>
              </div>
              <code style="font-size:.75rem;color:#a78bfa;">{rule['fol']}</code>
              <div style="margin-top:.5rem;font-size:.82rem;color:{p['text']};">
                📌 <b>{conds}</b> → <b>{dn(rule['disease'])}</b></div>
            </div>
            """, unsafe_allow_html=True)
        if lg["chains"]:
            with st.expander(f"📜 {t('mp_chains')} ({len(lg['chains'])})"):
                for chain in lg["chains"]:
                    st.code(chain, language="text")

    # ── Aksiyon butonları ────────────────────────────────────────────────
    st.markdown("---")
    ca, cb_ = st.columns(2)
    with ca:
        if st.button(f"🔄  {t('new_diag')}", use_container_width=True):
            st.session_state.results = None
            st.session_state.selected_symptoms = []
            go("symptoms")
    with cb_:
        if st.button(f"💾  {t('save')}", use_container_width=True):
            prof = st.session_state.profile
            st.session_state.history.append({
                "date":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "patient": f"{prof.get('name','?')} {prof.get('surname','')}".strip(),
                "top":     dn(diag[0]["name"]),
                "score":   diag[0]["final"],
                "sym_cnt": len(st.session_state.selected_symptoms),
            })
            st.success(t("saved_ok"))

    st.markdown(f"""
    <div style="background:{'rgba(230,179,67,.09)' if st.session_state.dark else 'rgba(217,119,6,.08)'};
         border:1px solid {p['warning']};border-radius:8px;padding:.65rem 1rem;
         text-align:center;font-size:.8rem;color:{p['warning']};margin-top:1rem;">
      {t('disclaimer')}</div>
    """, unsafe_allow_html=True)
