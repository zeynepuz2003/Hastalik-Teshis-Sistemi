"""
Logic Engine: First-Order Logic (FOL) kural tabanı ve Modus Ponens çıkarım motoru.

FOL Gösterimi:
  ∀x [ Belirti1(x) ∧ Belirti2(x) ∧ ... → OlasıHastalık(x) ]

Modus Ponens:
  Öncül 1 (Kural)    : P₁ ∧ P₂ ∧ ... → Q
  Öncül 2 (Gözlem)   : P₁ ∧ P₂ ∧ ... (hastada mevcut)
  Sonuç (Çıkarım)    : Q (hastalık muhtemel)
"""

from engine.knowledge_base import DISEASES

# ── FOL Kural Tabanı ────────────────────────────────────────────────────────
LOGIC_RULES = [
    # Grip
    {
        "id": "R01", "disease": "Grip (İnfluenza)",
        "name": "Grip — Klasik Üçlü",
        "conditions": ["ateş", "kas_ağrısı", "yorgunluk"],
        "confidence": 0.82,
        "fol": "∀x [Ateş(x) ∧ KasAğrısı(x) ∧ Yorgunluk(x) → OlasıGrip(x)]",
    },
    {
        "id": "R02", "disease": "Grip (İnfluenza)",
        "name": "Grip — Ateş + Üşüme",
        "conditions": ["ateş", "üşüme", "baş_ağrısı"],
        "confidence": 0.75,
        "fol": "∀x [Ateş(x) ∧ Üşüme(x) ∧ BaşAğrısı(x) → OlasıGrip(x)]",
    },
    # Nezle
    {
        "id": "R03", "disease": "Nezle",
        "name": "Nezle — Burun Belirtileri",
        "conditions": ["burun_akıntısı", "hapşırma"],
        "confidence": 0.78,
        "fol": "∀x [BurunAkıntısı(x) ∧ Hapşırma(x) → OlasıNezle(x)]",
    },
    {
        "id": "R04", "disease": "Nezle",
        "name": "Nezle — Boğaz + Burun",
        "conditions": ["boğaz_ağrısı", "burun_akıntısı", "öksürük"],
        "confidence": 0.72,
        "fol": "∀x [BoğazAğrısı(x) ∧ BurunAkıntısı(x) ∧ Öksürük(x) → OlasıNezle(x)]",
    },
    # COVID-19
    {
        "id": "R05", "disease": "COVID-19",
        "name": "COVID-19 — Solunum + Yorgunluk",
        "conditions": ["ateş", "öksürük", "nefes_darlığı"],
        "confidence": 0.85,
        "fol": "∀x [Ateş(x) ∧ Öksürük(x) ∧ NefesD.(x) → OlasıCOVID(x)]",
    },
    {
        "id": "R06", "disease": "COVID-19",
        "name": "COVID-19 — Yorgunluk Üçlüsü",
        "conditions": ["ateş", "yorgunluk", "kas_ağrısı"],
        "confidence": 0.70,
        "fol": "∀x [Ateş(x) ∧ Yorgunluk(x) ∧ KasAğrısı(x) → OlasıCOVID(x)]",
    },
    # Zatürre
    {
        "id": "R07", "disease": "Zatürre (Pnömoni)",
        "name": "Zatürre — Göğüs + Nefes",
        "conditions": ["ateş", "öksürük", "göğüs_ağrısı", "nefes_darlığı"],
        "confidence": 0.88,
        "fol": "∀x [Ateş(x) ∧ Öksürük(x) ∧ GöğüsAğrısı(x) ∧ NefesD.(x) → OlasıZatürre(x)]",
    },
    # Bronşit
    {
        "id": "R08", "disease": "Bronşit",
        "name": "Bronşit — Kronik Öksürük",
        "conditions": ["öksürük", "göğüs_ağrısı"],
        "confidence": 0.72,
        "fol": "∀x [Öksürük(x) ∧ GöğüsAğrısı(x) → OlasıBronşit(x)]",
    },
    # Astım
    {
        "id": "R09", "disease": "Astım",
        "name": "Astım — Nefes Darlığı",
        "conditions": ["nefes_darlığı", "öksürük", "göğüs_ağrısı"],
        "confidence": 0.80,
        "fol": "∀x [NefesD.(x) ∧ Öksürük(x) ∧ GöğüsAğrısı(x) → OlasıAstım(x)]",
    },
    # Diyabet
    {
        "id": "R10", "disease": "Diyabet (Tip 2)",
        "name": "Diyabet — Metabolik Üçlü",
        "conditions": ["aşırı_susama", "sık_idrara_çıkma", "yorgunluk"],
        "confidence": 0.90,
        "fol": "∀x [AşırıSusama(x) ∧ SıkİdraraÇıkma(x) ∧ Yorgunluk(x) → OlasıDiyabet(x)]",
    },
    {
        "id": "R11", "disease": "Diyabet (Tip 2)",
        "name": "Diyabet — Görme + Susama",
        "conditions": ["aşırı_susama", "bulanık_görme"],
        "confidence": 0.82,
        "fol": "∀x [AşırıSusama(x) ∧ BulanıkGörme(x) → OlasıDiyabet(x)]",
    },
    # Hipertansiyon
    {
        "id": "R12", "disease": "Hipertansiyon",
        "name": "Hipertansiyon — Baş + Çarpıntı",
        "conditions": ["baş_ağrısı", "baş_dönmesi", "çarpıntı"],
        "confidence": 0.78,
        "fol": "∀x [BaşAğrısı(x) ∧ BaşDönmesi(x) ∧ Çarpıntı(x) → OlasıHipertansiyon(x)]",
    },
    # Apandisit
    {
        "id": "R13", "disease": "Apandisit",
        "name": "Apandisit — Karın Ağrısı Üçlüsü",
        "conditions": ["karın_ağrısı", "ateş", "bulantı"],
        "confidence": 0.88,
        "fol": "∀x [KarınAğrısı(x) ∧ Ateş(x) ∧ Bulantı(x) → OlasıApandisit(x)]",
    },
    # Migren
    {
        "id": "R14", "disease": "Migren",
        "name": "Migren — Baş Ağrısı + Bulantı",
        "conditions": ["baş_ağrısı", "bulantı"],
        "confidence": 0.80,
        "fol": "∀x [BaşAğrısı(x) ∧ Bulantı(x) → OlasıMigren(x)]",
    },
    {
        "id": "R15", "disease": "Migren",
        "name": "Migren — Görme + Baş Dönmesi",
        "conditions": ["baş_ağrısı", "bulanık_görme", "baş_dönmesi"],
        "confidence": 0.75,
        "fol": "∀x [BaşAğrısı(x) ∧ BulanıkGörme(x) ∧ BaşDönmesi(x) → OlasıMigren(x)]",
    },
    # Gastrit
    {
        "id": "R16", "disease": "Gastrit",
        "name": "Gastrit — Mide Belirtileri",
        "conditions": ["karın_ağrısı", "bulantı", "iştahsızlık"],
        "confidence": 0.82,
        "fol": "∀x [KarınAğrısı(x) ∧ Bulantı(x) ∧ İştahsızlık(x) → OlasıGastrit(x)]",
    },
    # İYE
    {
        "id": "R17", "disease": "İdrar Yolu Enfeksiyonu",
        "name": "İYE — Üriner Belirtiler",
        "conditions": ["sık_idrara_çıkma", "sırt_ağrısı"],
        "confidence": 0.85,
        "fol": "∀x [SıkİdraraÇıkma(x) ∧ SırtAğrısı(x) → OlasıİYE(x)]",
    },
    # Anemi
    {
        "id": "R18", "disease": "Anemi",
        "name": "Anemi — Yorgunluk + Çarpıntı",
        "conditions": ["yorgunluk", "baş_dönmesi", "çarpıntı"],
        "confidence": 0.80,
        "fol": "∀x [Yorgunluk(x) ∧ BaşDönmesi(x) ∧ Çarpıntı(x) → OlasıAnemi(x)]",
    },
    # Hipotiroidizm
    {
        "id": "R19", "disease": "Hipotiroidizm",
        "name": "Tiroit — Yorgunluk + Üşüme",
        "conditions": ["yorgunluk", "üşüme", "kas_güçsüzlüğü"],
        "confidence": 0.78,
        "fol": "∀x [Yorgunluk(x) ∧ Üşüme(x) ∧ KasGüçsüzlüğü(x) → OlasıHipotiroid(x)]",
    },
    # Alerjik Rinit
    {
        "id": "R20", "disease": "Alerjik Rinit",
        "name": "Alerji — Göz + Burun",
        "conditions": ["hapşırma", "burun_akıntısı", "göz_kızarıklığı"],
        "confidence": 0.88,
        "fol": "∀x [Hapşırma(x) ∧ BurunAkıntısı(x) ∧ GözKızarıklığı(x) → OlasıAlerji(x)]",
    },
    # Suçiçeği
    {
        "id": "R21", "disease": "Suçiçeği",
        "name": "Suçiçeği — Döküntü + Ateş",
        "conditions": ["döküntü", "ateş", "iştahsızlık"],
        "confidence": 0.88,
        "fol": "∀x [Döküntü(x) ∧ Ateş(x) ∧ İştahsızlık(x) → OlasıSuçiçeği(x)]",
    },
    # Mononükleoz
    {
        "id": "R22", "disease": "Mononükleoz",
        "name": "Mono — Lenf + Boğaz",
        "conditions": ["şişmiş_lenf", "boğaz_ağrısı", "yorgunluk"],
        "confidence": 0.85,
        "fol": "∀x [ŞişmişLenf(x) ∧ BoğazAğrısı(x) ∧ Yorgunluk(x) → OlasıMono(x)]",
    },
    # Gıda Zehirlenmesi
    {
        "id": "R23", "disease": "Gıda Zehirlenmesi",
        "name": "Gıda Zeh. — GI Üçlüsü",
        "conditions": ["bulantı", "kusma", "ishal"],
        "confidence": 0.90,
        "fol": "∀x [Bulantı(x) ∧ Kusma(x) ∧ İshal(x) → OlasıGıdaZeh.(x)]",
    },
    {
        "id": "R24", "disease": "Gıda Zehirlenmesi",
        "name": "Gıda Zeh. — Karın + GI",
        "conditions": ["karın_ağrısı", "kusma", "ishal"],
        "confidence": 0.85,
        "fol": "∀x [KarınAğrısı(x) ∧ Kusma(x) ∧ İshal(x) → OlasıGıdaZeh.(x)]",
    },
]


def run_inference(selected_symptoms: list[str]) -> dict:
    """
    Modus Ponens ile çıkarım yapar.

    Her kural için:
      Öncül 1: koşul_kümesi → hastalık   (LOGIC_RULES'dan)
      Öncül 2: koşul_kümesi ⊆ seçili_belirtiler
      Sonuç  : hastalık → ateş edildi

    Döndürür:
      - fired_rules   : ateşlenen kurallar listesi
      - disease_scores: hastalık → max güven skoru
      - chains        : Modus Ponens zincir gösterimi
    """
    symptom_set = set(selected_symptoms)
    fired_rules: list[dict] = []
    disease_scores: dict[str, float] = {}
    chains: list[str] = []

    for rule in LOGIC_RULES:
        cond_set = set(rule["conditions"])
        if cond_set.issubset(symptom_set):
            fired_rules.append(rule)
            d = rule["disease"]
            disease_scores[d] = max(disease_scores.get(d, 0.0), rule["confidence"])

            # Modus Ponens zinciri
            premise = " ∧ ".join(rule["conditions"])
            chain = (
                f"[{rule['id']}] Öncül 1 (Kural): {rule['fol']}\n"
                f"        Öncül 2 (Gözlem): {premise} — hastada mevcut\n"
                f"        Sonuç           : {d} olasılığı (güven: {rule['confidence']:.0%})"
            )
            chains.append(chain)

    return {
        "fired_rules": fired_rules,
        "disease_scores": disease_scores,
        "chains": chains,
    }
