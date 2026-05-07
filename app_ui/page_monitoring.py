"""
Sayfa: İzleme & Değerlendirme — canlı ajan istatistikleri, otomatik test, detay logu.
"""

import streamlit as st

from engine.logic_engine import run_inference
from engine.probability  import hybrid_scores

from app_ui.theme      import palette
from app_ui.helpers    import t, dn, sl, go
from app_ui.components import score_bar

# ── Bilinen test senaryoları ──────────────────────────────────────────────────
EVAL_CASES = [
    (["ateş","öksürük","nefes_darlığı"],               "COVID-19"),
    (["ateş","kas_ağrısı","yorgunluk","üşüme"],         "Grip (İnfluenza)"),
    (["burun_akıntısı","hapşırma","boğaz_ağrısı"],      "Nezle"),
    (["bulantı","kusma","ishal","karın_ağrısı"],        "Gıda Zehirlenmesi"),
    (["aşırı_susama","sık_idrara_çıkma","yorgunluk"],   "Diyabet (Tip 2)"),
    (["baş_ağrısı","bulantı","baş_dönmesi"],            "Migren"),
    (["hapşırma","burun_akıntısı","göz_kızarıklığı"],   "Alerjik Rinit"),
    (["ateş","öksürük","göğüs_ağrısı","nefes_darlığı"],"Zatürre (Pnömoni)"),
    (["yorgunluk","baş_dönmesi","çarpıntı"],            "Anemi"),
    (["baş_ağrısı","baş_dönmesi","çarpıntı"],           "Hipertansiyon"),
]


def _run_eval_cases():
    """Test senaryolarını çalıştırır; top-1 ve top-3 doğruluğunu döndürür."""
    results = []
    top1_ok = top3_ok = 0
    for syms, expected in EVAL_CASES:
        lr      = run_inference(syms)
        mr      = hybrid_scores(selected=syms, logic_disease_scores=lr["disease_scores"])
        sorted_d = sorted(mr["scores"].items(), key=lambda x: x[1]["final"], reverse=True)
        top3    = [d[0] for d in sorted_d[:3]]
        top1    = top3[0]
        ok1     = (top1 == expected)
        ok3     = (expected in top3)
        if ok1: top1_ok += 1
        if ok3: top3_ok += 1
        results.append({
            "symptoms":  syms, "expected": expected,
            "predicted": top1, "score": round(sorted_d[0][1]["final"] * 100, 1),
            "top3": top3, "ok1": ok1, "ok3": ok3,
        })
    n = len(EVAL_CASES)
    return results, round(top1_ok / n * 100, 1), round(top3_ok / n * 100, 1)


def page_monitoring():
    p     = palette()
    is_tr = (st.session_state.lang == "TR")
    log   = st.session_state.monitor_log

    st.markdown(f"""
    <div style="background:{p['surface']};border:1px solid {p['border']};
         border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1.3rem;
         box-shadow:{p['shadow_sm']};">
      <div style="font-size:1.1rem;font-weight:800;color:{p['accent']};">
        📈 {'Ajan İzleme & Değerlendirme' if is_tr else 'Agent Monitoring & Evaluation'}
      </div>
      <div style="font-size:.82rem;color:{p['muted']};margin-top:.25rem;">
        {'Teşhis oturumlarının canlı performans analizi ve matematiksel değerlendirme.'
         if is_tr else
         'Live performance analysis and mathematical evaluation of diagnosis sessions.'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab_live, tab_eval, tab_log = st.tabs([
        f"📊 {'Canlı İstatistikler' if is_tr else 'Live Statistics'}",
        f"🧪 {'Otomatik Değerlendirme' if is_tr else 'Automatic Evaluation'}",
        f"📝 {'Ajan Logu' if is_tr else 'Agent Log'}",
    ])

    # ════════════════════════════════════════════════════════════════════
    # TAB 1 — Canlı İstatistikler
    # ════════════════════════════════════════════════════════════════════
    with tab_live:
        if not log:
            st.info("Henüz teşhis yapılmadı. Belirti seçip Teşhis Al'a basınca burası dolacak."
                    if is_tr else
                    "No diagnoses yet. Run a diagnosis and stats will appear here.")
        else:
            import pandas as pd
            from collections import Counter

            n           = len(log)
            avg_score   = round(sum(e["score"]       for e in log) / n, 1)
            avg_improve = round(sum(e["opt_improve"]  for e in log) / n, 1)
            avg_rules   = round(sum(e["rules_fired"]  for e in log) / n, 1)
            avg_iters   = round(sum(e["opt_iters"]    for e in log) / n)
            conv_rate   = round(sum(1 for e in log if e["opt_conv"]) / n * 100, 1)

            kpi_data = [
                ("🔬", str(n),            "Toplam Teşhis"  if is_tr else "Total Sessions"),
                ("🎯", f"{avg_score}%",   "Ort. Güven"     if is_tr else "Avg Confidence"),
                ("⚡", f"+{avg_improve}%","Ort. İyileşme"   if is_tr else "Avg Improvement"),
                ("📐", f"{avg_rules}",    "Ort. Kural"      if is_tr else "Avg Rules Fired"),
                ("🔄", f"{avg_iters}",    "Ort. İterasyon"  if is_tr else "Avg Iterations"),
                ("✅", f"%{conv_rate}",   "Yakınsama Oranı" if is_tr else "Convergence Rate"),
            ]
            for col, (icon, val, lbl) in zip(st.columns(6), kpi_data):
                with col:
                    st.markdown(f"""
                    <div style="background:{p['surface2']};border:1px solid {p['border']};
                         border-radius:10px;padding:.8rem .4rem;text-align:center;margin-bottom:.8rem;">
                      <div style="font-size:1.4rem;">{icon}</div>
                      <div style="font-size:1.25rem;font-weight:800;color:{p['accent']};
                           line-height:1.1;">{val}</div>
                      <div style="font-size:.65rem;color:{p['muted']};margin-top:3px;
                           text-transform:uppercase;letter-spacing:.05em;">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"**📉 {'Güven Trendi' if is_tr else 'Confidence Trend'}**")
            df_trend = pd.DataFrame({
                "Hybrid %":  [e["score"]   for e in log],
                "Bayes %":   [e["bayes"]   for e in log],
                "Cosine %":  [e["cosine"]  for e in log],
                "Logic %":   [e["logic_s"] for e in log],
            })
            st.line_chart(df_trend, height=220, use_container_width=True)

            st.markdown(f"**📊 {'Ort. Bileşen Katkısı' if is_tr else 'Avg Component Contribution'}**")
            avg_b = round(sum(e["bayes"]   for e in log) / n, 1)
            avg_c = round(sum(e["cosine"]  for e in log) / n, 1)
            avg_l = round(sum(e["logic_s"] for e in log) / n, 1)
            st.markdown(
                score_bar("Bayes (α=0.50)", avg_b, p["success"]) +
                score_bar("Cosine (β=0.30)", avg_c, "#a78bfa") +
                score_bar("Logic (γ=0.20)", avg_l, p["warning"]),
                unsafe_allow_html=True,
            )

            st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**🏥 {'Hastalık Dağılımı' if is_tr else 'Disease Distribution'}**")
                df_dis = pd.DataFrame.from_dict(
                    Counter(dn(e["top"]) for e in log),
                    orient="index", columns=["Count"]
                ).sort_values("Count", ascending=False)
                st.bar_chart(df_dis, height=220, use_container_width=True)
            with col_b:
                st.markdown(f"**⚡ {'Optimizasyon Trendi' if is_tr else 'Optimization Trend'}**")
                df_opt = pd.DataFrame({
                    "Initial %": [e["opt_init"]  for e in log],
                    "Final %":   [e["opt_final"] for e in log],
                })
                st.line_chart(df_opt, height=220, use_container_width=True)

            all_rule_ids = [rid for e in log for rid in e["rule_ids"]]
            if all_rule_ids:
                st.markdown(f"**🔗 {'En Sık FOL Kuralları' if is_tr else 'Top FOL Rules'}**")
                df_rules = pd.DataFrame.from_dict(
                    Counter(all_rule_ids), orient="index", columns=["Fires"]
                ).sort_values("Fires", ascending=False).head(10)
                st.bar_chart(df_rules, height=200, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════
    # TAB 2 — Otomatik Değerlendirme
    # ════════════════════════════════════════════════════════════════════
    with tab_eval:
        st.markdown(f"""
        <div style="background:{'rgba(79,142,247,.08)' if st.session_state.dark else 'rgba(37,99,235,.05)'};
             border:1px solid {p['accent']};border-radius:10px;padding:.9rem 1.2rem;
             margin-bottom:1.2rem;font-size:.85rem;color:{p['muted']};">
          {'🧪 <b>Otomatik Değerlendirme:</b> 10 bilinen vaka üzerinde Top-1 ve Top-3 doğruluğu ölçülür.'
           if is_tr else
           '🧪 <b>Automatic Evaluation:</b> Measures Top-1 and Top-3 accuracy on 10 known cases.'}
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶  " + ("Değerlendirmeyi Çalıştır" if is_tr else "Run Evaluation"),
                     type="primary"):
            with st.spinner("Değerlendiriliyor…"):
                st.session_state.eval_results = _run_eval_cases()

        ev = st.session_state.eval_results
        if ev:
            cases, top1_acc, top3_acc = ev

            for col, val, lbl, color in zip(
                st.columns(3),
                [f"{top1_acc}%", f"{top3_acc}%", str(len(cases))],
                ["Top-1 Doğruluk" if is_tr else "Top-1 Accuracy",
                 "Top-3 Doğruluk" if is_tr else "Top-3 Accuracy",
                 "Test Senaryosu" if is_tr else "Test Scenarios"],
                [p["success"], p["accent"], p["muted"]],
            ):
                with col:
                    st.markdown(f"""
                    <div style="background:{p['surface2']};border:2px solid {color};
                         border-radius:12px;padding:1.1rem;text-align:center;margin-bottom:.8rem;">
                      <div style="font-size:2rem;font-weight:900;color:{color};">{val}</div>
                      <div style="font-size:.75rem;color:{p['muted']};text-transform:uppercase;
                           letter-spacing:.06em;margin-top:4px;">{lbl}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"**{'Test Senaryoları' if is_tr else 'Test Scenarios'}**")
            for i, c in enumerate(cases):
                ok_icon  = "✅" if c["ok1"] else ("🟡" if c["ok3"] else "❌")
                border_c = p["success"] if c["ok1"] else (p["warning"] if c["ok3"] else "#f85149")
                sym_str  = ", ".join(sl(s) for s in c["symptoms"])
                st.markdown(f"""
                <div style="background:{p['surface']};border-left:4px solid {border_c};
                     border:1px solid {p['border']};border-left:4px solid {border_c};
                     border-radius:10px;padding:.9rem 1.1rem;margin-bottom:.6rem;">
                  <div style="display:flex;justify-content:space-between;
                       align-items:flex-start;flex-wrap:wrap;gap:.4rem;">
                    <div style="flex:1;">
                      <div style="font-size:.72rem;color:{p['muted']};margin-bottom:.3rem;">
                        #{i+1} · {sym_str}</div>
                      <div style="font-size:.88rem;">
                        <span style="color:{p['muted']};">{'Beklenen' if is_tr else 'Expected'}:</span>
                        <b style="color:{p['text']};"> {dn(c['expected'])}</b></div>
                      <div style="font-size:.88rem;margin-top:.2rem;">
                        <span style="color:{p['muted']};">{'Tahmin' if is_tr else 'Predicted'}:</span>
                        <b style="color:{border_c};"> {dn(c['predicted'])}</b>
                        <span style="font-size:.78rem;color:{p['muted']};"> ({c['score']}%)</span>
                      </div>
                    </div>
                    <div style="font-size:1.6rem;align-self:center;">{ok_icon}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            correct = sum(1 for c in cases if c["ok1"])
            top3_n  = sum(1 for c in cases if c["ok3"])
            st.markdown(
                f"**📐 {'Matematiksel Değerlendirme' if is_tr else 'Mathematical Evaluation'}**  \n"
                f"Top-1 Accuracy = {correct}/{len(cases)} = **{top1_acc}%**  \n"
                f"Top-3 Accuracy = {top3_n}/{len(cases)} = **{top3_acc}%**  \n"
                f"{'Yanlış sınıf:' if is_tr else 'Misclassified:'} "
                f"{len(cases)-correct}  \n"
                f"Hibrit skor: α·Bayes(0.5) + β·Cosine(0.3) + γ·Logic(0.2)"
            )

    # ════════════════════════════════════════════════════════════════════
    # TAB 3 — Ajan Logu
    # ════════════════════════════════════════════════════════════════════
    with tab_log:
        if not log:
            st.info("Teşhis logu boş." if is_tr else "Agent log is empty.")
        else:
            import pandas as pd
            rows = [{
                "#": i,
                "Saat/Time":            e["ts"],
                "Belirti/Symptoms":     e["n_sym"],
                "Teşhis/Diagnosis":     dn(e["top"]),
                "Hibrit %":             e["score"],
                "Bayes %":              e["bayes"],
                "Cosine %":             e["cosine"],
                "Logic %":              e["logic_s"],
                "Kural/Rules":          e["rules_fired"],
                "Init %":               e["opt_init"],
                "Final %":              e["opt_final"],
                "İyileşme/Improve %":   e["opt_improve"],
                "İter.":                e["opt_iters"],
                "Yakınsama/Conv.":      "✅" if e["opt_conv"] else "❌",
            } for i, e in enumerate(log, 1)]
            st.dataframe(pd.DataFrame(rows).set_index("#"),
                         use_container_width=True, height=380)

            if st.button("🗑️ " + ("Logu Temizle" if is_tr else "Clear Log")):
                st.session_state.monitor_log  = []
                st.session_state.eval_results = None
                st.rerun()

    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    if st.button(f"← {'Geri' if is_tr else 'Back'}", key="mon_back"):
        go("results" if st.session_state.results else "welcome")
