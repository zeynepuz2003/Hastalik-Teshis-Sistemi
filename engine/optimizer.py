"""
Hill Climbing Optimizasyon Modülü

Amaç: Belirti ağırlık vektörü w ∈ ℝ^|S| optimize ederek
      teşhis sisteminin güvenini (confidence) maksimize etmek.

Objektif Fonksiyon:
  f(w) = (en_yüksek_skor - ikinci_skor) / (en_yüksek_skor + ε)
         — iki en olası hastalık arasındaki ayrım oranı

Algoritma:
  1. Başlangıç: w₀ = [1, 1, ..., 1]
  2. Her adımda rastgele bir boyut seç, ±δ pertürbasyon uygula
  3. f(w_yeni) > f(w_mevcut) ise kabul et (steepest ascent)
  4. N adım sonra veya iyileşme durduğunda bitir

Kısıt: w[j] ∈ [0.1, 3.0] — belirtileri tamamen yok saymadan
"""

import numpy as np
from engine.knowledge_base import ALL_SYMPTOMS, DISEASES
from engine.probability import build_matrix, patient_vector, bayesian_scores, cosine_similarities


def _objective(M: np.ndarray, v_weighted: np.ndarray,
               logic_scores: np.ndarray, alpha: float, beta: float, gamma: float) -> float:
    """
    Mevcut ağırlık vektörü için objektif değeri hesapla.
    Yüksek değer → teşhis daha özgün / güvenilir.
    """
    eps = 1e-9

    b = bayesian_scores(M, v_weighted)
    c = cosine_similarities(M, v_weighted)
    c_min, c_max = c.min(), c.max()
    c_norm = (c - c_min) / (c_max - c_min + eps)

    l_max = logic_scores.max() if logic_scores.max() > 0 else 1.0
    l_norm = logic_scores / (l_max + eps)

    combined = alpha * b + beta * c_norm + gamma * l_norm
    exp_c = np.exp(combined - combined.max())
    final = exp_c / (exp_c.sum() + eps)

    sorted_f = np.sort(final)[::-1]
    if sorted_f[0] < eps:
        return 0.0
    return float((sorted_f[0] - sorted_f[1]) / (sorted_f[0] + eps))


def hill_climbing(
    selected_symptoms: list[str],
    logic_disease_scores: dict[str, float],
    max_iter: int = 300,
    step_size: float = 0.15,
    w_min: float = 0.1,
    w_max: float = 3.0,
    alpha: float = 0.50,
    beta: float = 0.30,
    gamma: float = 0.20,
    seed: int = 42,
) -> dict:
    """
    Hill Climbing ile belirti ağırlıklarını optimize eder.

    Döndürür:
      weights       : optimize edilmiş ağırlık vektörü (|S| boyutlu)
      history       : her iterasyondaki objektif değer listesi
      initial_score : başlangıç objektif değeri
      final_score   : son objektif değeri
      improvement   : mutlak iyileşme
      converged     : True ise erken durma
      best_symptom_weights: belirti_adı → ağırlık sözlüğü
    """
    rng = np.random.default_rng(seed)
    M   = build_matrix()
    v   = patient_vector(selected_symptoms)
    diseases = list(DISEASES.keys())
    l_scores = np.array([logic_disease_scores.get(d, 0.0) for d in diseases])

    # Belirtiler seçilmediyse anlamsız — sıfır döndür
    if v.sum() == 0:
        return {
            "weights": np.ones(len(ALL_SYMPTOMS)).tolist(),
            "history": [0.0],
            "initial_score": 0.0,
            "final_score": 0.0,
            "improvement": 0.0,
            "converged": False,
            "best_symptom_weights": {s: 1.0 for s in ALL_SYMPTOMS},
        }

    w = np.ones(len(ALL_SYMPTOMS))
    current_score = _objective(M, v * w, l_scores, alpha, beta, gamma)
    initial_score = current_score

    history = [current_score]
    no_improve = 0
    patience = 50   # ardışık iyileşmesiz adım sayısı

    for iteration in range(max_iter):
        # Rastgele bir boyut seç
        idx = rng.integers(0, len(ALL_SYMPTOMS))
        direction = rng.choice([-1, 1])
        delta = direction * step_size

        w_new = w.copy()
        w_new[idx] = float(np.clip(w_new[idx] + delta, w_min, w_max))

        new_score = _objective(M, v * w_new, l_scores, alpha, beta, gamma)

        if new_score > current_score:
            w = w_new
            current_score = new_score
            no_improve = 0
        else:
            no_improve += 1

        history.append(current_score)

        if no_improve >= patience:
            converged = True
            break
    else:
        converged = False

    best_weights = {ALL_SYMPTOMS[j]: float(w[j]) for j in range(len(ALL_SYMPTOMS))}

    return {
        "weights": w.tolist(),
        "history": history,
        "initial_score": float(initial_score),
        "final_score": float(current_score),
        "improvement": float(current_score - initial_score),
        "converged": converged,
        "iterations_run": len(history) - 1,
        "best_symptom_weights": best_weights,
    }
