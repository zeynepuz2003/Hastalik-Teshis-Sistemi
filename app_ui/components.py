"""
Paylaşılan UI bileşenleri: banner, adım göstergesi, hasta bilgi çubuğu, skor barı.
"""

import streamlit as st

from app_ui.theme import palette
from app_ui.helpers import t, go


def render_banner():
    """Üst navigasyon çubuğu: logo, breadcrumb, tema/dil/geçmiş/izleme butonları."""
    p = palette()
    theme_icon = "☀️" if st.session_state.dark else "🌙"
    theme_tip  = "Açık Temaya Geç" if st.session_state.dark else "Koyu Temaya Geç"

    left, mid, r1, r2, r3, r4 = st.columns([4.5, 2, 0.65, 0.65, 0.65, 0.65])

    with left:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;
             background:{p['surface']};border:1px solid {p['border']};
             border-radius:12px;padding:0.65rem 1.1rem;box-shadow:{p['shadow_sm']};">
          <span style="font-size:1.85rem;line-height:1;">🏥</span>
          <div>
            <div style="font-size:1rem;font-weight:700;color:{p['accent']};line-height:1.25;">
              DiagnosisAI
            </div>
            <div style="font-size:0.7rem;color:{p['muted']};">{t('app_subtitle')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with mid:
        page_icons = {
            "welcome":    "🏠 Ana Sayfa"  if st.session_state.lang == "TR" else "🏠 Home",
            "profile":    "👤 Profil"     if st.session_state.lang == "TR" else "👤 Profile",
            "symptoms":   "🩺 Belirtiler" if st.session_state.lang == "TR" else "🩺 Symptoms",
            "results":    "📊 Sonuçlar"   if st.session_state.lang == "TR" else "📊 Results",
            "history":    "📋 Geçmiş"     if st.session_state.lang == "TR" else "📋 History",
            "monitoring": "📈 İzleme"     if st.session_state.lang == "TR" else "📈 Monitoring",
        }
        crumb = page_icons.get(st.session_state.page, "")
        n_log = len(st.session_state.monitor_log)
        badge = f" · {n_log}" if n_log > 0 else ""
        st.markdown(f"""
        <div style="display:flex;align-items:center;height:100%;
             padding:0.65rem 0.8rem;background:{p['surface2']};
             border:1px solid {p['border']};border-radius:10px;
             font-size:0.8rem;font-weight:500;color:{p['muted']};">
          {crumb}<span style="color:{p['accent']};margin-left:4px;">{badge}</span>
        </div>
        """, unsafe_allow_html=True)

    with r1:
        if st.button(theme_icon, key="btn_theme", help=theme_tip, use_container_width=True):
            st.session_state.dark = not st.session_state.dark
            st.rerun()
    with r2:
        if st.button(t("lang_btn"), key="btn_lang", help="Switch Language", use_container_width=True):
            st.session_state.lang = "EN" if st.session_state.lang == "TR" else "TR"
            st.rerun()
    with r3:
        if st.button("📋", key="btn_hist", help=t("hist_title"), use_container_width=True):
            go("history")
    with r4:
        if st.button("📈", key="btn_mon", help="Monitoring & Evaluation", use_container_width=True):
            go("monitoring")

    st.markdown("<div style='height:.2rem'></div>", unsafe_allow_html=True)


def render_steps(current: str):
    """Profil → Belirtiler → Sonuçlar adım göstergesi."""
    p = palette()
    steps = ["profile", "symptoms", "results"]
    labels = (["Profile", "Symptoms", "Results"]
              if st.session_state.lang == "EN"
              else ["Profil", "Belirtiler", "Sonuçlar"])

    try:
        cur_idx = steps.index(current)
    except ValueError:
        cur_idx = -1

    items = ""
    for i, (_, lbl) in enumerate(zip(steps, labels)):
        if i < cur_idx:
            circ = f"background:{p['success']};border-color:{p['success']};color:#fff;"
            icon = "✓"
        elif i == cur_idx:
            circ = (f"background:{p['accent']};border-color:{p['accent']};color:#fff;"
                    f"box-shadow:0 0 0 4px {p['accent']}33;")
            icon = str(i + 1)
        else:
            circ = f"background:{p['surface2']};border-color:{p['border']};color:{p['muted']};"
            icon = str(i + 1)

        label_col = p["accent"] if i == cur_idx else p["muted"]
        label_w   = "700"      if i == cur_idx else "400"
        conn_bg   = p["success"] if i < cur_idx else p["border"]
        conn = (f'<div style="flex:1;height:2px;background:{conn_bg};margin-bottom:20px;"></div>'
                if i < len(steps) - 1 else "")

        items += f"""
        <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
          <div style="width:34px;height:34px;border-radius:50%;border:2px solid;
               display:flex;align-items:center;justify-content:center;
               font-size:.85rem;font-weight:600;{circ}">{icon}</div>
          <div style="font-size:.7rem;margin-top:4px;color:{label_col};
               font-weight:{label_w};text-align:center;">{lbl}</div>
        </div>{conn}"""

    st.markdown(
        f'<div style="display:flex;align-items:center;max-width:500px;'
        f'margin:0 auto 1.4rem auto;">{items}</div>',
        unsafe_allow_html=True,
    )


def render_patient_bar():
    """Aktif hasta bilgilerini üst bilgi çubuğunda gösterir."""
    p    = palette()
    prof = st.session_state.profile
    if not prof:
        return

    name   = f"{prof.get('name','?')} {prof.get('surname','')}".strip()
    age    = prof.get("age", "?")
    gender = prof.get("gender", "?")
    pain   = prof.get("pain_val", "")
    dur    = prof.get("duration", "")
    role   = t("role_doctor") if st.session_state.role == "doctor" else t("role_patient")

    fields = [
        ("👤", t("patient_lbl"), name),
        ("🎂", t("age"),         str(age)),
        ("⚥",  t("gender"),      gender),
        ("🏷️", t("role_lbl"),    role),
    ]
    if dur:
        fields.append(("⏱️", t("duration"), dur))
    if pain != "":
        fields.append(("💊", t("pain"), f"{pain}/10"))

    cells = "".join(f"""
    <div style="display:flex;flex-direction:column;padding:0 1rem;
         border-right:1px solid {p['border']};">
      <span style="font-size:.62rem;text-transform:uppercase;letter-spacing:.06em;
            color:{p['muted']};">{icon} {label}</span>
      <span style="font-size:.9rem;font-weight:600;color:{p['text']};margin-top:1px;">{val}</span>
    </div>
    """ for icon, label, val in fields)

    st.markdown(f"""
    <div style="background:{p['surface']};border:1px solid {p['border']};
         border-radius:10px;padding:.6rem .4rem;display:flex;
         align-items:center;gap:.2rem;flex-wrap:wrap;
         margin-bottom:1.2rem;box-shadow:{p['shadow_sm']};">
      {cells}
    </div>
    """, unsafe_allow_html=True)


def score_bar(label: str, value: float, color: str, suffix: str = "%") -> str:
    """HTML skor çubuğu döndürür (st.markdown ile kullanılır)."""
    pct = min(max(float(value), 0), 100)
    return f"""
<div style="margin:5px 0;">
  <div style="display:flex;justify-content:space-between;
       font-size:.8rem;color:#8b949e;margin-bottom:2px;">
    <span>{label}</span><span>{value:.1f}{suffix}</span>
  </div>
  <div style="height:7px;border-radius:4px;background:#21262d;overflow:hidden;">
    <div style="height:100%;width:{pct}%;background:{color};border-radius:4px;
         transition:width .5s ease;"></div>
  </div>
</div>"""
