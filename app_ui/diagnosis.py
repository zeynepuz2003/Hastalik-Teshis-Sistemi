"""
Teşhis motoru: logic + optimizasyon + hibrit skor zinciri.
"""

import numpy as np

from engine.knowledge_base import DISEASES, SYMPTOM_LABELS
from engine.logic_engine    import run_inference
from engine.probability     import hybrid_scores
from engine.optimizer       import hill_climbing


def run_diagnosis(selected: list[str]) -> dict:
    """
    Seçili belirtiler için tam teşhis akışını çalıştırır:
      1. FOL + Modus Ponens çıkarımı
      2. Hill Climbing ağırlık optimizasyonu
      3. Hibrit skor (Bayes + Kosinüs + Mantık)

    Döndürür: diagnoses, math, optim, logic alt-sözlükleri
    """
    logic_result = run_inference(selected)
    opt_result   = hill_climbing(
        selected_symptoms=selected,
        logic_disease_scores=logic_result["disease_scores"],
        max_iter=300, step_size=0.15,
    )
    weights     = np.array(opt_result["weights"])
    math_result = hybrid_scores(
        selected=selected,
        logic_disease_scores=logic_result["disease_scores"],
        weights=weights,
    )

    scores   = math_result["scores"]
    sorted_d = sorted(scores.items(), key=lambda x: x[1]["final"], reverse=True)

    diagnoses = []
    for rank, (dname, ds) in enumerate(sorted_d[:8]):
        info    = DISEASES[dname]
        matched = [s for s in selected if s in info["symptoms"]]
        fired   = [
            {"id": r["id"], "name": r["name"], "fol": r["fol"],
             "confidence": r["confidence"]}
            for r in logic_result["fired_rules"] if r["disease"] == dname
        ]
        diagnoses.append({
            "rank": rank + 1, "name": dname,
            "description": info["description"], "color": info["color"],
            "final":  round(ds["final"]  * 100, 1),
            "bayes":  round(ds["bayes"]  * 100, 2),
            "cosine": round(ds["cosine"] * 100, 2),
            "logic":  round(ds["logic"]  * 100, 2),
            "matched": matched, "fired": fired,
        })

    top_w = {
        SYMPTOM_LABELS[s]: round(opt_result["best_symptom_weights"][s], 3)
        for s in selected if s in opt_result["best_symptom_weights"]
    }

    return {
        "diagnoses": diagnoses,
        "math": {
            "mat_norm":  round(math_result["matrix_norm"], 3),
            "vec_norm":  round(math_result["symptom_vector_norm"], 3),
            "eigenvals": [round(e, 3) for e in math_result["top_eigenvalues"]],
            "variance":  [round(e * 100, 1) for e in math_result["explained_variance"]],
            "n_sym":     math_result["n_symptoms_selected"],
        },
        "optim": {
            "init":      round(opt_result["initial_score"] * 100, 1),
            "final":     round(opt_result["final_score"]   * 100, 1),
            "improve":   round(opt_result["improvement"]   * 100, 1),
            "iters":     opt_result["iterations_run"],
            "converged": opt_result["converged"],
            "history":   [round(h * 100, 2) for h in opt_result["history"]],
            "weights":   top_w,
        },
        "logic": {
            "fired_count": len(logic_result["fired_rules"]),
            "chains":      logic_result["chains"],
            "rules": [
                {"id": r["id"], "name": r["name"], "disease": r["disease"],
                 "fol": r["fol"], "confidence": round(r["confidence"] * 100),
                 "conditions": r["conditions"]}
                for r in logic_result["fired_rules"]
            ],
        },
    }
