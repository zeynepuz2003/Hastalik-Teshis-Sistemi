# Hastalık Teşhis Uzman Sistemi

Yapay Zeka Temelli Tıbbi Karar Destek Sistemi — Principles of AI Grup Projesi

## Özellikler

- **18 hastalık**, **29 belirti** tanımlı bilgi tabanı
- **First-Order Logic + Modus Ponens** çıkarım motoru (24 kural)
- **Bayesian çıkarım** + **Linear Algebra** (matris, kosinüs benzerliği, özdeğer analizi)
- **Hill Climbing** optimizasyonu ile belirti ağırlıkları otomatik ayarlanır
- Sonuçları görselleştiren modern web arayüzü

## Kurulum

```bash
pip install flask numpy
python3 app.py
```

Tarayıcıda aç: `http://localhost:5050`

## Teknik Yapı

```
├── app.py                  # Flask sunucusu
├── engine/
│   ├── knowledge_base.py   # Hastalık & belirti veritabanı
│   ├── logic_engine.py     # FOL kuralları + Modus Ponens
│   ├── probability.py      # Bayes + Linear Algebra
│   └── optimizer.py        # Hill Climbing
├── templates/index.html    # Arayüz
└── static/                 # CSS & JS
```

## AI Bileşenleri

### 1. Logic — First-Order Logic
Modus Ponens ile çıkarım:
```
∀x [Ateş(x) ∧ KasAğrısı(x) ∧ Yorgunluk(x) → OlasıGrip(x)]
```

### 2. Math of AI — Bayes + Linear Algebra
- Semptom-Hastalık Matrisi **M** (18×29): `M[i][j] = P(belirti_j | hastalık_i)`
- Hasta vektörü **v** ∈ {0,1}²⁹
- Bayes skoru: `P(H|v) ∝ P(v|H) · P(H)`
- Kosinüs benzerliği: `cos(Mᵢ, v) = (Mᵢ · v) / (‖Mᵢ‖₂ · ‖v‖₂)`
- MᵀM kovaryans matrisinden özdeğer analizi (PCA)

### 3. Optimization — Hill Climbing
Belirti ağırlık vektörü **w**'yu optimize eder:
```
f(w) = (skor₁ - skor₂) / skor₁    → maksimize et
```
Her iterasyonda rastgele bir ağırlık ±δ kaydırılır, iyileşirse kabul edilir.
