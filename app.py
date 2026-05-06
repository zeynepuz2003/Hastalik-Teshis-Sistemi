"""
Hastalık Teşhis Uzman Sistemi — Flask Uygulaması
"""

import numpy as np
from flask import Flask, render_template, request, jsonify

from engine.knowledge_base import DISEASES, SYMPTOM_LABELS, SYMPTOM_GROUPS, ALL_SYMPTOMS
from engine.logic_engine   import run_inference
from engine.probability    import hybrid_scores
from engine.optimizer      import hill_climbing

app = Flask(__name__)


@app.route("/")
def index():
    symptom_groups = {}
    for group, symptoms in SYMPTOM_GROUPS.items():
        symptom_groups[group] = [
            {"key": s, "label": SYMPTOM_LABELS[s]} for s in symptoms
        ]
    return render_template("index.html", symptom_groups=symptom_groups)


@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.get_json()
    selected: list[str] = data.get("symptoms", [])

    if not selected:
        return jsonify({"error": "En az bir belirti seçiniz."}), 400

    # ── 1. Mantık Motoru (FOL + Modus Ponens) ──────────────────────────────
    logic_result = run_inference(selected)

    # ── 2. Hill Climbing Optimizasyonu ─────────────────────────────────────
    opt_result = hill_climbing(
        selected_symptoms=selected,
        logic_disease_scores=logic_result["disease_scores"],
        max_iter=300,
        step_size=0.15,
    )

    # ── 3. Hibrit Olasılık Hesabı (Bayes + Linear Algebra) ─────────────────
    weights = np.array(opt_result["weights"])
    math_result = hybrid_scores(
        selected=selected,
        logic_disease_scores=logic_result["disease_scores"],
        weights=weights,
    )

    # ── 4. Sonuçları Derle ─────────────────────────────────────────────────
    scores = math_result["scores"]
    sorted_diseases = sorted(scores.items(), key=lambda x: x[1]["final"], reverse=True)

    diagnoses = []
    for rank, (d_name, d_scores) in enumerate(sorted_diseases[:8]):
        info = DISEASES[d_name]

        # Hangi belirtiler bu hastalıkla eşleşiyor?
        matched = [s for s in selected if s in info["symptoms"]]

        # Hangi mantık kuralları ateşlendi?
        fired = [
            {"id": r["id"], "name": r["name"], "fol": r["fol"],
             "confidence": r["confidence"]}
            for r in logic_result["fired_rules"]
            if r["disease"] == d_name
        ]

        diagnoses.append({
            "rank":        rank + 1,
            "name":        d_name,
            "short":       info["short"],
            "description": info["description"],
            "color":       info["color"],
            "final_score": round(d_scores["final"] * 100, 1),
            "bayes_score": round(d_scores["bayes"] * 100, 2),
            "cosine_sim":  round(d_scores["cosine"], 4),
            "logic_score": round(d_scores["logic"], 3),
            "matched_symptoms": [SYMPTOM_LABELS[s] for s in matched],
            "logic_rules": fired,
        })

    # Modus Ponens zincirlerini metinleştir
    mp_chains = logic_result["chains"]

    # Önemli ağırlıklar (sadece seçili belirtiler)
    top_weights = {
        SYMPTOM_LABELS[s]: round(opt_result["best_symptom_weights"][s], 3)
        for s in selected if s in opt_result["best_symptom_weights"]
    }

    response = {
        "diagnoses": diagnoses,
        "math": {
            "matrix_frobenius_norm": round(math_result["matrix_norm"], 3),
            "symptom_vector_norm":   round(math_result["symptom_vector_norm"], 3),
            "top_eigenvalues":       [round(e, 3) for e in math_result["top_eigenvalues"]],
            "explained_variance":    [round(e * 100, 1) for e in math_result["explained_variance"]],
            "n_symptoms_selected":   math_result["n_symptoms_selected"],
        },
        "optimization": {
            "initial_score":    round(opt_result["initial_score"] * 100, 1),
            "final_score":      round(opt_result["final_score"] * 100, 1),
            "improvement":      round(opt_result["improvement"] * 100, 1),
            "iterations_run":   opt_result["iterations_run"],
            "converged":        opt_result["converged"],
            "history":          [round(h * 100, 2) for h in opt_result["history"]],
            "top_weights":      top_weights,
        },
        "logic": {
            "rules_fired_count": len(logic_result["fired_rules"]),
            "modus_ponens_chains": mp_chains,
            "fired_rules": [
                {
                    "id": r["id"], "name": r["name"],
                    "disease": r["disease"], "fol": r["fol"],
                    "confidence": round(r["confidence"] * 100, 0),
                    "conditions": [SYMPTOM_LABELS[c] for c in r["conditions"]],
                }
                for r in logic_result["fired_rules"]
            ],
        },
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
