"""
Probability & Linear Algebra Modülü

Matematiksel Temel:
1. Semptom-Hastalık Matrisi M (|D| × |S|)
   M[i][j] = P(belirti_j | hastalık_i)

2. Hasta Vektörü v ∈ {0,1}^|S|
   v[j] = 1 ise belirti_j hastada mevcut

3. Bayes Teoremi ile Olasılık:
   P(H_i | v) ∝ P(v | H_i) · P(H_i)
   Log-uzayında: log_score(i) = Σ_j [v_j · log(M[i][j]) + (1-v_j)·log(1-M[i][j])]

4. Kosinüs Benzerliği:
   cos(M_i, v) = (M_i · v) / (‖M_i‖₂ · ‖v‖₂)

5. Hibrit Skor:
   score(i) = α · bayes_prob(i) + β · cosine_sim(i) + γ · logic_score(i)
   α=0.5, β=0.3, γ=0.2
"""

import numpy as np
from engine.knowledge_base import DISEASES, ALL_SYMPTOMS


def build_matrix() -> np.ndarray:
    """M matrisini oluşturur: satır=hastalık, sütun=belirti."""
    diseases = list(DISEASES.keys())
    M = np.zeros((len(diseases), len(ALL_SYMPTOMS)))
    for i, d in enumerate(diseases):
        for j, s in enumerate(ALL_SYMPTOMS):
            M[i, j] = DISEASES[d]["symptoms"].get(s, 0.02)
    return M


def patient_vector(selected: list[str]) -> np.ndarray:
    """Seçili belirtilerden ikili hasta vektörü oluşturur."""
    v = np.zeros(len(ALL_SYMPTOMS))
    for j, s in enumerate(ALL_SYMPTOMS):
        if s in selected:
            v[j] = 1.0
    return v


def bayesian_scores(M: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Log-Bayes skoru hesaplar:
      log_score(i) = Σ_j [v_j·log(M[i,j]) + (1-v_j)·log(1-M[i,j])] + log(prior_i)
    Döndürülen değerler softmax ile normalize edilir → olasılık dağılımı.
    """
    diseases = list(DISEASES.keys())
    eps = 1e-9
    log_scores = np.zeros(len(diseases))
    for i, d in enumerate(diseases):
        p_d = DISEASES[d]["prior"]
        log_p = np.log(p_d + eps)
        for j in range(len(ALL_SYMPTOMS)):
            p_s_given_d = M[i, j]
            if v[j] == 1:
                log_p += np.log(p_s_given_d + eps)
            else:
                log_p += np.log(1 - p_s_given_d + eps)
        log_scores[i] = log_p

    # Sayısal kararlılık için en yüksekten kaydır
    log_scores -= np.max(log_scores)
    raw = np.exp(log_scores)
    return raw / (raw.sum() + eps)


def cosine_similarities(M: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Her hastalık satırı ile hasta vektörü arasında kosinüs benzerliği."""
    eps = 1e-9
    v_norm = np.linalg.norm(v) + eps
    sims = np.zeros(M.shape[0])
    for i in range(M.shape[0]):
        row_norm = np.linalg.norm(M[i]) + eps
        sims[i] = np.dot(M[i], v) / (row_norm * v_norm)
    return sims


def compute_pca_info(M: np.ndarray) -> dict:
    """
    Semptom-hastalık matrisinden PCA benzeri istatistikler.
    MᵀM kovaryans matrisinin ilk 3 özdeğer/özvektörü döndürülür.
    """
    cov = M.T @ M  # |S| × |S|
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    # Büyükten küçüğe sırala
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    explained = eigenvalues[:3] / (eigenvalues.sum() + 1e-9)
    return {
        "top_eigenvalues": eigenvalues[:3].tolist(),
        "explained_variance": explained.tolist(),
        "matrix_norm": float(np.linalg.norm(M, "fro")),
        "top_eigenvector": eigenvectors[:, 0].tolist(),
    }


def hybrid_scores(
    selected: list[str],
    logic_disease_scores: dict[str, float],
    weights: np.ndarray | None = None,
    alpha: float = 0.50,
    beta: float = 0.30,
    gamma: float = 0.20,
) -> dict:
    """
    Üç kaynağı birleştiren hibrit skor:
      score(i) = α·bayes(i) + β·cosine(i) + γ·logic(i)

    İsteğe bağlı belirti ağırlık vektörü (Hill Climbing'den) desteklenir.
    """
    M = build_matrix()
    v = patient_vector(selected)

    if weights is not None:
        # Ağırlıklı hasta vektörü
        v_w = v * weights
    else:
        v_w = v

    b_scores = bayesian_scores(M, v_w)
    c_sims   = cosine_similarities(M, v_w)

    # Kosinüsü [0,1] aralığına al
    c_min, c_max = c_sims.min(), c_sims.max()
    if c_max > c_min:
        c_norm = (c_sims - c_min) / (c_max - c_min)
    else:
        c_norm = np.zeros_like(c_sims)

    diseases = list(DISEASES.keys())
    l_scores = np.array([
        logic_disease_scores.get(d, 0.0) for d in diseases
    ])
    l_max = l_scores.max() if l_scores.max() > 0 else 1.0
    l_norm = l_scores / l_max

    combined = alpha * b_scores + beta * c_norm + gamma * l_norm

    # Softmax ile normalize et
    exp_c = np.exp(combined - combined.max())
    final = exp_c / exp_c.sum()

    result = {}
    for i, d in enumerate(diseases):
        result[d] = {
            "final": float(final[i]),
            "bayes": float(b_scores[i]),
            "cosine": float(c_sims[i]),
            "logic": float(l_scores[i]),
        }

    pca_info = compute_pca_info(M)

    return {
        "scores": result,
        "matrix_norm": pca_info["matrix_norm"],
        "top_eigenvalues": pca_info["top_eigenvalues"],
        "explained_variance": pca_info["explained_variance"],
        "symptom_vector_norm": float(np.linalg.norm(v)),
        "n_symptoms_selected": int(v.sum()),
    }
