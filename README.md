# 🏥 Disease Diagnosis Expert System

> **AI-Powered Clinical Decision Support** — A rational agent that perceives symptoms, reasons through logic and probability, and returns differential diagnoses ranked by confidence.

---

## Overview

This project implements a multi-pillar AI expert system for disease diagnosis. It was built as an academic assignment demonstrating three foundational AI techniques working together in a single pipeline:

| Pillar | Implementation |
|--------|---------------|
| **Logic** | First-Order Logic (FOL) rule base + Modus Ponens inference engine |
| **Math of AI** | Bayesian scoring, cosine similarity, PCA / eigenvalue analysis (Linear Algebra) |
| **Optimization** | Hill Climbing on symptom weight vectors |

The system covers **18 diseases**, **29 symptoms**, and **24 FOL rules**. A full-featured Streamlit UI supports both patient and clinician workflows in Turkish and English, with dark/light theming and live monitoring.

---

## Screenshots

| Welcome Page | Symptom Selection | Diagnosis Results |
|---|---|---|
| Animated hero, system stats, role selector | Grouped checkboxes, real-time count | Top diagnosis banner + 4-tab detail view |

| Monitoring Dashboard | Automatic Evaluation |
|---|---|
| Live KPI cards, confidence trend, FOL rule frequency | 10 preset test cases, Top-1/Top-3 accuracy |

---

## Architecture

```
streamlit_app.py          ← Entry point (35 lines)
│
├── app_ui/               ← UI layer
│   ├── translations.py   ← TR / EN string dictionaries
│   ├── theme.py          ← Dark / light palette + global CSS
│   ├── helpers.py        ← Session state, t(), dn(), sl(), go()
│   ├── components.py     ← Banner, step indicator, patient bar, score bar
│   ├── diagnosis.py      ← Full diagnosis pipeline wrapper
│   ├── page_welcome.py   ← Animated landing page + role selection
│   ├── page_profile.py   ← Patient personal information form
│   ├── page_symptoms.py  ← Symptom selection (grouped checkboxes)
│   ├── page_results.py   ← 4-tab results: diagnoses / math / optim / logic
│   ├── page_history.py   ← Saved diagnosis history
│   └── page_monitoring.py← Live stats, automatic evaluation, agent log
│
├── engine/               ← AI core (framework-independent)
│   ├── knowledge_base.py ← 18 diseases, 29 symptoms, priors, P(s|d) matrix
│   ├── logic_engine.py   ← FOL rules + Modus Ponens inference
│   ├── probability.py    ← Bayesian scoring, cosine similarity, PCA
│   └── optimizer.py      ← Hill Climbing weight optimisation
│
├── app.py                ← Flask REST API (alternative backend)
├── templates/index.html  ← Flask HTML frontend
└── requirements.txt
```

---

## AI Pipeline

```
User selects symptoms
        │
        ▼
┌─────────────────────┐
│  1. Logic Engine    │  FOL rules → Modus Ponens → disease_scores dict
│  (logic_engine.py)  │  24 rules, up to 0.90 confidence
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  2. Hill Climbing   │  Optimises symptom weight vector w ∈ ℝ²⁹
│  (optimizer.py)     │  Objective: maximise (top_score − 2nd_score) / top_score
│                     │  Constraints: w[j] ∈ [0.1, 3.0], max 300 iterations
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  3. Hybrid Score    │  score(i) = α·Bayes(i) + β·Cosine(i) + γ·Logic(i)
│  (probability.py)   │  α=0.50, β=0.30, γ=0.20
│                     │  + PCA / Frobenius norm metadata
└────────┬────────────┘
         │
         ▼
  Ranked differential diagnoses (top 8)
```

### Mathematical Foundation

**Bayesian Score (log-space)**
```
log P(Hᵢ | v) ∝ log P(Hᵢ) + Σⱼ [ vⱼ·log P(sⱼ|Hᵢ) + (1−vⱼ)·log(1−P(sⱼ|Hᵢ)) ]
```

**Cosine Similarity**
```
cos(Mᵢ, v) = (Mᵢ · v) / (‖Mᵢ‖₂ · ‖v‖₂)
```

**Hill Climbing Objective**
```
f(w) = (score₁ − score₂) / (score₁ + ε)   — maximise separation between top two diseases
```

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/zeynepuz2003/Hastalik-Teshis-Sistemi.git
cd Hastalik-Teshis-Sistemi

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the Streamlit UI

```bash
streamlit run streamlit_app.py
```

Open **http://localhost:8501** in your browser.

### Run the Flask API (optional)

```bash
python app.py
```

Open **http://localhost:5050** in your browser.

---

## Usage Flow

```
Welcome Page  →  Select role (Patient / Doctor)
     ↓
Profile Form  →  Name, age, gender, blood type, pain level, complaint duration
     ↓
Symptom Page  →  Check symptoms grouped by category
     ↓
Results Page  →  Top diagnosis banner + 4 detail tabs
     ↓
Save to History  or  New Diagnosis
```

### Results Tabs

| Tab | Contents |
|-----|----------|
| **All Diagnoses** | Ranked list of up to 8 diseases with score breakdown |
| **Math Details** | Frobenius norm, eigenvalues, explained variance (PCA), symptom vector norm |
| **Optimization** | Hill Climbing convergence chart, symptom weight ranking |
| **Logic / FOL** | Fired rules with full FOL notation and Modus Ponens chains |

### Monitoring Page (`📈` button in top bar)

| Sub-tab | Contents |
|---------|----------|
| **Live Statistics** | Session KPIs, confidence trend, score component contribution, disease distribution, FOL rule frequency |
| **Automatic Evaluation** | Runs 10 preset test scenarios, reports Top-1 and Top-3 accuracy |
| **Agent Log** | Full session-by-session data table |

---

## Project Structure Details

### `engine/` — AI Core

| File | Responsibility |
|------|---------------|
| `knowledge_base.py` | Disease definitions: `P(symptom \| disease)` matrix, prior probabilities, symptom groups |
| `logic_engine.py` | 24 FOL rules; `run_inference()` returns fired rules and Modus Ponens chains |
| `probability.py` | `hybrid_scores()` — Bayes + cosine + logic; `compute_pca_info()` — eigenvalue decomposition |
| `optimizer.py` | `hill_climbing()` — iterative symptom weight optimisation with early stopping |

### `app_ui/` — UI Layer

Each file is independently owned and can be developed separately:

| File | Role |
|------|------|
| `translations.py` | All user-facing strings in TR and EN |
| `theme.py` | Dark / light color palette and global CSS injection |
| `helpers.py` | Shared utilities: session state init, translation lookup, navigation |
| `components.py` | Reusable widgets: top banner, step indicator, patient info bar, score bar |
| `diagnosis.py` | Thin wrapper that calls the engine pipeline and formats results for the UI |
| `page_*.py` | One file per page — fully independent, easy to assign to different team members |

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥ 1.35 | Web UI framework |
| `numpy` | ≥ 1.26 | Matrix operations, probability calculations |
| `pandas` | ≥ 2.0 | Monitoring charts and log table |
| `flask` | ≥ 3.0 | Alternative REST API backend |

---

## Team Roles

| Role | Responsibilities |
|------|-----------------|
| Project Manager | Coordination, timeline, documentation |
| Lead Developer | Engine integration, `streamlit_app.py`, `app_ui/diagnosis.py` |
| UI/UX Designer | `page_welcome.py`, `theme.py`, CSS animations |
| Mathematical Modeler | `engine/probability.py`, `engine/knowledge_base.py` |
| Logic Engineer | `engine/logic_engine.py`, FOL rules, Modus Ponens chains |
| Evaluation & Optimization Specialist | `engine/optimizer.py`, `app_ui/page_monitoring.py` |

---

## License

This project was developed for academic purposes. All rights reserved by the project team.
