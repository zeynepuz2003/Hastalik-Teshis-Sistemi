"""
Sayfa: Karşılama / Ana Sayfa — animasyonlu hero, istatistikler, özellik kartları, rol seçimi.
"""

import streamlit as st

from app_ui.theme   import palette
from app_ui.helpers import t, go


def page_welcome():
    p       = palette()
    is_dark = st.session_state.dark

    # ── Animasyon CSS ──────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @keyframes floatUpDown {
      0%,100% { transform: translateY(0px); }
      50%      { transform: translateY(-12px); }
    }
    @keyframes fadeInUp {
      from { opacity:0; transform:translateY(28px); }
      to   { opacity:1; transform:translateY(0); }
    }
    @keyframes fadeInLeft {
      from { opacity:0; transform:translateX(-24px); }
      to   { opacity:1; transform:translateX(0); }
    }
    @keyframes fadeInRight {
      from { opacity:0; transform:translateX(24px); }
      to   { opacity:1; transform:translateX(0); }
    }
    @keyframes pulseGlow {
      0%,100% { box-shadow: 0 0 0 0 rgba(79,142,247,0); }
      50%      { box-shadow: 0 0 32px 8px rgba(79,142,247,0.25); }
    }
    @keyframes gradientFlow {
      0%   { background-position: 0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    @keyframes countUp {
      from { opacity:0; transform:scale(.7); }
      to   { opacity:1; transform:scale(1); }
    }
    @keyframes blink {
      0%,100% { opacity:1; } 50% { opacity:0; }
    }
    .hero-icon       { animation: floatUpDown 3.2s ease-in-out infinite; display:inline-block; }
    .hero-title      { animation: fadeInUp .8s ease both; }
    .hero-sub        { animation: fadeInUp 1s ease .15s both; }
    .hero-badge      { animation: fadeInUp 1s ease .3s both; }
    .feat-card-left  { animation: fadeInLeft .7s ease both; }
    .feat-card-right { animation: fadeInRight .7s ease both; }
    .stat-item       { animation: countUp .6s ease both; }
    .role-card-hover { transition: transform .25s, box-shadow .25s, border-color .25s; }
    .role-card-hover:hover { transform: translateY(-5px) scale(1.02); }
    .pulse-ring      { animation: pulseGlow 2.5s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────
    hero_bg  = "rgba(79,142,247,0.06)"  if is_dark else "rgba(37,99,235,0.04)"
    hero_brd = "rgba(79,142,247,0.18)"  if is_dark else "rgba(37,99,235,0.15)"
    tag_bg   = "rgba(79,142,247,0.15)"  if is_dark else "rgba(37,99,235,0.10)"

    title = ("Disease Diagnosis Expert System" if st.session_state.lang == "EN"
             else "Hastalık Teşhis Uzman Sistemi")
    sub   = ("AI · Bayesian · Logic Engine · Hill Climbing Optimization"
             if st.session_state.lang == "EN"
             else "Yapay Zeka · Bayes · Mantık Motoru · Hill Climbing Optimizasyonu")
    tag   = ("⚡ Real-Time Analysis" if st.session_state.lang == "EN"
             else "⚡ Gerçek Zamanlı Analiz")

    st.markdown(f"""
    <div style="background:{hero_bg};border:1px solid {hero_brd};
         border-radius:24px;padding:3.2rem 2rem 2.8rem;text-align:center;
         margin-bottom:2rem;position:relative;overflow:hidden;">
      <div style="position:absolute;top:-60px;left:-60px;width:220px;height:220px;
           border-radius:50%;background:radial-gradient(circle,rgba(79,142,247,.12),transparent);
           pointer-events:none;"></div>
      <div style="position:absolute;bottom:-40px;right:-40px;width:180px;height:180px;
           border-radius:50%;background:radial-gradient(circle,rgba(124,58,237,.10),transparent);
           pointer-events:none;"></div>
      <div class="hero-icon" style="font-size:5rem;margin-bottom:1rem;
           filter:drop-shadow(0 8px 24px rgba(79,142,247,.4));">🏥</div>
      <div class="hero-badge" style="display:inline-block;background:{tag_bg};
           border:1px solid {p['accent']};color:{p['accent']};border-radius:20px;
           padding:4px 16px;font-size:.78rem;font-weight:600;margin-bottom:1rem;
           letter-spacing:.04em;">{tag}</div>
      <h1 class="hero-title" style="font-size:2.6rem;font-weight:900;margin:.4rem 0 .8rem;
           background:linear-gradient(270deg,#4f8ef7,#a78bfa,#38bdf8,#4f8ef7);
           background-size:300% 300%;-webkit-background-clip:text;
           -webkit-text-fill-color:transparent;
           animation:gradientFlow 5s ease infinite,fadeInUp .8s ease both;">{title}</h1>
      <p class="hero-sub" style="color:{p['muted']};font-size:.92rem;
           max-width:540px;margin:0 auto .6rem;line-height:1.7;">{sub}</p>
      <span style="display:inline-block;width:2px;height:1.1rem;
            background:{p['accent']};border-radius:2px;vertical-align:middle;
            animation:blink 1.1s step-end infinite;margin-left:2px;"></span>
    </div>
    """, unsafe_allow_html=True)

    # ── İstatistik kartları ───────────────────────────────────────────────
    stats = ([("18","Diseases"),("29","Symptoms"),("24","FOL Rules"),("3","Algorithms")]
             if st.session_state.lang == "EN"
             else [("18","Hastalık"),("29","Belirti"),("24","FOL Kuralı"),("3","Algoritma")])
    for col, (num, lbl) in zip(st.columns(4), stats):
        with col:
            st.markdown(f"""
            <div class="stat-item" style="background:{p['surface']};border:1px solid {p['border']};
                 border-radius:14px;padding:1.1rem .5rem;text-align:center;
                 box-shadow:{p['shadow_sm']};margin-bottom:1rem;">
              <div style="font-size:2.2rem;font-weight:900;
                   background:{p['grad']};-webkit-background-clip:text;
                   -webkit-text-fill-color:transparent;line-height:1.1;">{num}</div>
              <div style="font-size:.75rem;color:{p['muted']};font-weight:500;
                   text-transform:uppercase;letter-spacing:.07em;margin-top:4px;">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Özellik kartları ──────────────────────────────────────────────────
    feats = ([
        ("🧠","Bayesian Inference",
         "Log-space probability computation models symptom-disease relationships. "
         "Prior knowledge and conditional probabilities are combined."),
        ("🔗","First-Order Logic (FOL)",
         "Modus Ponens inference engine with 24 rule base for instant reasoning. "
         "Every result is explained by a logical chain."),
        ("📐","Linear Algebra & Cosine",
         "Vector similarity on the symptom-disease matrix, PCA eigenvalue analysis "
         "and Frobenius norm computations."),
        ("⚡","Hill Climbing Optimization",
         "Symptom weight vector is iteratively optimized to maximize diagnosis "
         "confidence. Converges within 300 iterations."),
    ] if st.session_state.lang == "EN" else [
        ("🧠","Bayes Teoremine Dayalı",
         "Log-uzayında olasılık hesabı ile belirti-hastalık ilişkisi modellenir. "
         "Prior bilgisi ve koşullu olasılıklar birleştirilir."),
        ("🔗","First-Order Logic (FOL)",
         "Modus Ponens çıkarım motoru ile 24 kural tabanından anlık akıl yürütme. "
         "Her sonuç mantıksal zincirle açıklanır."),
        ("📐","Lineer Cebir & Kosinüs",
         "Semptom-hastalık matrisi üzerinde vektör benzerliği, PCA özdeğer analizi "
         "ve Frobenius norm hesapları yapılır."),
        ("⚡","Hill Climbing Optimizasyon",
         "Belirti ağırlık vektörü iteratif olarak optimize edilerek teşhis "
         "güveni maksimize edilir. 300 iterasyonda yakınsama."),
    ])

    feat_title = "How It Works" if st.session_state.lang == "EN" else "Sistem Nasıl Çalışır?"
    st.markdown(f"""
    <div style="text-align:center;margin:1.5rem 0 1rem;">
      <span style="font-size:1.1rem;font-weight:700;color:{p['text']};">{feat_title}</span>
      <div style="width:48px;height:3px;background:{p['grad']};border-radius:2px;
           margin:.4rem auto 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2 = st.columns(2, gap="medium")
    for i, (col, (icon, head, body)) in enumerate(zip([fc1, fc2, fc1, fc2], feats)):
        anim  = "feat-card-left" if i % 2 == 0 else "feat-card-right"
        delay = f"{i * 0.12:.2f}s"
        with col:
            st.markdown(f"""
            <div class="{anim}" style="background:{p['surface']};border:1px solid {p['border']};
                 border-radius:14px;padding:1.3rem 1.4rem;margin-bottom:.9rem;
                 box-shadow:{p['shadow_sm']};animation-delay:{delay};
                 border-left:3px solid {p['accent']};">
              <div style="font-size:1.6rem;margin-bottom:.5rem;">{icon}</div>
              <div style="font-size:.95rem;font-weight:700;color:{p['text']};
                   margin-bottom:.4rem;">{head}</div>
              <div style="font-size:.8rem;color:{p['muted']};line-height:1.6;">{body}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Rol seçimi ────────────────────────────────────────────────────────
    role_title = ("How Would You Like to Continue?" if st.session_state.lang == "EN"
                  else "Nasıl Devam Etmek İstersiniz?")
    st.markdown(f"""
    <div style="text-align:center;margin:2rem 0 1.2rem;">
      <span style="font-size:1.1rem;font-weight:700;color:{p['text']};">{role_title}</span>
      <div style="width:48px;height:3px;background:{p['grad']};border-radius:2px;
           margin:.4rem auto 0;"></div>
    </div>
    """, unsafe_allow_html=True)

    roles = [
        ("patient","🤒","role_patient","role_patient_desc","btn_patient",
         "#f85149" if is_dark else "#dc2626",
         "rgba(248,81,73,.10)" if is_dark else "rgba(220,38,38,.07)"),
        ("doctor","👨‍⚕️","role_doctor","role_doctor_desc","btn_doctor",
         p["accent"],
         "rgba(79,142,247,.10)" if is_dark else "rgba(37,99,235,.07)"),
    ]
    for col, (role_key, icon, title_k, desc_k, btn_k, ac, bg_c) in zip(st.columns(2, gap="large"), roles):
        with col:
            st.markdown(f"""
            <div class="role-card-hover pulse-ring" style="background:{bg_c};
                 border:2px solid {ac};border-radius:20px;
                 padding:2.2rem 1.5rem 1.5rem;text-align:center;margin-bottom:.8rem;">
              <div style="font-size:3.8rem;margin-bottom:.8rem;
                   filter:drop-shadow(0 4px 12px {ac}55);">{icon}</div>
              <div style="font-size:1.25rem;font-weight:800;color:{ac};
                   margin-bottom:.5rem;">{t(title_k)}</div>
              <div style="font-size:.85rem;color:{p['muted']};line-height:1.6;">{t(desc_k)}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{icon}  {t(title_k)}  —  {t('continue')}",
                         key=btn_k, use_container_width=True):
                st.session_state.role = role_key
                go("profile")

    st.markdown(f"""
    <div style="background:{'rgba(230,179,67,.08)' if is_dark else 'rgba(217,119,6,.07)'};
         border:1px solid {p['warning']};border-radius:10px;padding:.8rem 1.2rem;
         text-align:center;font-size:.8rem;color:{p['warning']};
         margin-top:1.8rem;line-height:1.6;">{t('disclaimer')}</div>
    """, unsafe_allow_html=True)
