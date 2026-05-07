"""
Knowledge Base: 18 hastalık ve 29 belirti tanımı.
Her belirti için P(belirti | hastalık) olasılıkları ve prior olasılıklar.
"""

SYMPTOM_LABELS = {
    "ateş":               "Ateş",
    "öksürük":            "Öksürük",
    "yorgunluk":          "Yorgunluk / Halsizlik",
    "baş_ağrısı":         "Baş Ağrısı",
    "kas_ağrısı":         "Kas Ağrısı",
    "üşüme":              "Üşüme / Titreme",
    "boğaz_ağrısı":       "Boğaz Ağrısı",
    "burun_akıntısı":     "Burun Akıntısı",
    "hapşırma":           "Hapşırma",
    "nefes_darlığı":      "Nefes Darlığı",
    "göğüs_ağrısı":       "Göğüs Ağrısı",
    "bulantı":            "Bulantı",
    "kusma":              "Kusma",
    "karın_ağrısı":       "Karın Ağrısı",
    "ishal":              "İshal",
    "baş_dönmesi":        "Baş Dönmesi",
    "iştahsızlık":        "İştah Kaybı",
    "döküntü":            "Döküntü / Kızarıklık",
    "eklem_ağrısı":       "Eklem Ağrısı",
    "aşırı_susama":       "Aşırı Susama",
    "sık_idrara_çıkma":   "Sık İdrara Çıkma",
    "bulanık_görme":      "Bulanık Görme",
    "gece_terlemesi":     "Gece Terlemesi",
    "şişmiş_lenf":        "Şişmiş Lenf Bezleri",
    "kas_güçsüzlüğü":     "Kas Güçsüzlüğü",
    "sırt_ağrısı":        "Sırt / Bel Ağrısı",
    "göz_kızarıklığı":    "Göz Kızarıklığı",
    "sarılık":            "Sarılık (Cilt/Göz)",
    "çarpıntı":           "Çarpıntı",
}

ALL_SYMPTOMS = list(SYMPTOM_LABELS.keys())

SYMPTOM_GROUPS = {
    "Genel / Sistemik": [
        "ateş", "yorgunluk", "kas_güçsüzlüğü", "kas_ağrısı",
        "üşüme", "gece_terlemesi", "iştahsızlık",
    ],
    "Solunum Sistemi": [
        "öksürük", "nefes_darlığı", "göğüs_ağrısı",
        "boğaz_ağrısı", "burun_akıntısı", "hapşırma",
    ],
    "Nörolojik / Baş": [
        "baş_ağrısı", "baş_dönmesi", "bulanık_görme",
    ],
    "Sindirim Sistemi": [
        "bulantı", "kusma", "ishal", "karın_ağrısı",
    ],
    "Deri / Lenf": [
        "döküntü", "şişmiş_lenf", "göz_kızarıklığı", "sarılık",
    ],
    "Kardiyovasküler / Diğer": [
        "çarpıntı", "eklem_ağrısı", "sırt_ağrısı",
    ],
    "Üriner / Metabolik": [
        "aşırı_susama", "sık_idrara_çıkma",
    ],
}

# P(belirti | hastalık) değerleri — tıbbi literatüre dayalı tahmini olasılıklar
DISEASES = {
    "Grip (İnfluenza)": {
        "short": "Grip",
        "description": "İnfluenza virüsünün neden olduğu akut solunum yolu enfeksiyonu.",
        "symptoms": {
            "ateş": 0.92, "öksürük": 0.82, "yorgunluk": 0.88,
            "baş_ağrısı": 0.72, "kas_ağrısı": 0.85, "üşüme": 0.78,
            "boğaz_ağrısı": 0.55, "burun_akıntısı": 0.42, "iştahsızlık": 0.62,
        },
        "prior": 0.15,
        "color": "#e74c3c",
    },
    "Nezle": {
        "short": "Nezle",
        "description": "Rhinovirus kaynaklı üst solunum yolu enfeksiyonu.",
        "symptoms": {
            "burun_akıntısı": 0.92, "hapşırma": 0.88, "boğaz_ağrısı": 0.78,
            "öksürük": 0.62, "ateş": 0.18, "yorgunluk": 0.42, "baş_ağrısı": 0.35,
        },
        "prior": 0.20,
        "color": "#3498db",
    },
    "COVID-19": {
        "short": "COVID-19",
        "description": "SARS-CoV-2 virüsünün neden olduğu akut solunum yolu hastalığı.",
        "symptoms": {
            "ateş": 0.88, "öksürük": 0.78, "yorgunluk": 0.88,
            "nefes_darlığı": 0.72, "baş_ağrısı": 0.68, "kas_ağrısı": 0.72,
            "iştahsızlık": 0.58, "ishal": 0.32, "döküntü": 0.18, "üşüme": 0.45,
        },
        "prior": 0.10,
        "color": "#9b59b6",
    },
    "Zatürre (Pnömoni)": {
        "short": "Zatürre",
        "description": "Akciğerlerin bakteri veya virüs kaynaklı iltihaplanması.",
        "symptoms": {
            "ateş": 0.90, "öksürük": 0.85, "nefes_darlığı": 0.82,
            "göğüs_ağrısı": 0.75, "yorgunluk": 0.80, "üşüme": 0.70,
            "iştahsızlık": 0.55, "kas_ağrısı": 0.48,
        },
        "prior": 0.07,
        "color": "#e67e22",
    },
    "Bronşit": {
        "short": "Bronşit",
        "description": "Bronş tüplerinin iltihaplanması; kronik öksürük ile seyreder.",
        "symptoms": {
            "öksürük": 0.92, "göğüs_ağrısı": 0.68, "yorgunluk": 0.65,
            "nefes_darlığı": 0.58, "ateş": 0.45, "boğaz_ağrısı": 0.42,
        },
        "prior": 0.08,
        "color": "#1abc9c",
    },
    "Astım": {
        "short": "Astım",
        "description": "Kronik hava yolu iltihabı; nefes almayı zorlaştırır.",
        "symptoms": {
            "nefes_darlığı": 0.92, "öksürük": 0.82, "göğüs_ağrısı": 0.72,
            "yorgunluk": 0.55, "hapşırma": 0.45, "burun_akıntısı": 0.40,
        },
        "prior": 0.08,
        "color": "#2ecc71",
    },
    "Diyabet (Tip 2)": {
        "short": "Diyabet",
        "description": "Kronik yüksek kan şekeri; insülin direnci ile karakterizedir.",
        "symptoms": {
            "aşırı_susama": 0.92, "sık_idrara_çıkma": 0.90, "yorgunluk": 0.80,
            "bulanık_görme": 0.68, "kas_güçsüzlüğü": 0.62, "iştahsızlık": 0.42,
            "baş_dönmesi": 0.45,
        },
        "prior": 0.09,
        "color": "#f39c12",
    },
    "Hipertansiyon": {
        "short": "Hipertansiyon",
        "description": "Kronik yüksek tansiyon; kalp-damar hastalığı riskini artırır.",
        "symptoms": {
            "baş_ağrısı": 0.72, "baş_dönmesi": 0.68, "çarpıntı": 0.62,
            "nefes_darlığı": 0.48, "yorgunluk": 0.45, "bulanık_görme": 0.38,
            "bulantı": 0.32,
        },
        "prior": 0.12,
        "color": "#c0392b",
    },
    "Apandisit": {
        "short": "Apandisit",
        "description": "Apandiksin iltihaplanması; acil cerrahi müdahale gerektirir.",
        "symptoms": {
            "karın_ağrısı": 0.95, "ateş": 0.78, "bulantı": 0.82,
            "kusma": 0.72, "iştahsızlık": 0.85, "yorgunluk": 0.55,
        },
        "prior": 0.04,
        "color": "#922b21",
    },
    "Migren": {
        "short": "Migren",
        "description": "Şiddetli tekrarlayan baş ağrısı; nörolojik semptomlarla eşlik edebilir.",
        "symptoms": {
            "baş_ağrısı": 0.95, "bulantı": 0.75, "kusma": 0.58,
            "baş_dönmesi": 0.62, "yorgunluk": 0.68, "bulanık_görme": 0.45,
            "iştahsızlık": 0.52,
        },
        "prior": 0.10,
        "color": "#8e44ad",
    },
    "Gastrit": {
        "short": "Gastrit",
        "description": "Mide mukozasının iltihaplanması; mide rahatsızlığına yol açar.",
        "symptoms": {
            "karın_ağrısı": 0.88, "bulantı": 0.82, "kusma": 0.68,
            "iştahsızlık": 0.75, "baş_ağrısı": 0.42, "yorgunluk": 0.48,
        },
        "prior": 0.08,
        "color": "#16a085",
    },
    "İdrar Yolu Enfeksiyonu": {
        "short": "İYE",
        "description": "Üretral veya mesane enfeksiyonu; kadınlarda daha yaygındır.",
        "symptoms": {
            "sık_idrara_çıkma": 0.90, "sırt_ağrısı": 0.72, "ateş": 0.65,
            "karın_ağrısı": 0.62, "yorgunluk": 0.52, "bulantı": 0.38,
        },
        "prior": 0.07,
        "color": "#2980b9",
    },
    "Anemi": {
        "short": "Anemi",
        "description": "Kanda kırmızı kan hücresi / hemoglobin eksikliği.",
        "symptoms": {
            "yorgunluk": 0.90, "baş_dönmesi": 0.82, "kas_güçsüzlüğü": 0.75,
            "çarpıntı": 0.68, "nefes_darlığı": 0.58, "baş_ağrısı": 0.55,
            "iştahsızlık": 0.48,
        },
        "prior": 0.09,
        "color": "#7f8c8d",
    },
    "Hipotiroidizm": {
        "short": "Tiroit",
        "description": "Tiroit bezinin yetersiz hormon üretmesi; metabolizmayı yavaşlatır.",
        "symptoms": {
            "yorgunluk": 0.88, "kas_güçsüzlüğü": 0.78, "kas_ağrısı": 0.65,
            "iştahsızlık": 0.55, "baş_dönmesi": 0.48, "üşüme": 0.72,
            "gece_terlemesi": 0.35, "çarpıntı": 0.38,
        },
        "prior": 0.07,
        "color": "#27ae60",
    },
    "Alerjik Rinit": {
        "short": "Alerji",
        "description": "Alerjen maddelere karşı bağışıklık sisteminin aşırı tepkisi.",
        "symptoms": {
            "hapşırma": 0.92, "burun_akıntısı": 0.90, "göz_kızarıklığı": 0.82,
            "öksürük": 0.55, "baş_ağrısı": 0.45, "yorgunluk": 0.42,
            "döküntü": 0.32,
        },
        "prior": 0.12,
        "color": "#d4ac0d",
    },
    "Suçiçeği": {
        "short": "Suçiçeği",
        "description": "Varicella-zoster virüsünün neden olduğu döküntülü viral enfeksiyon.",
        "symptoms": {
            "döküntü": 0.95, "ateş": 0.85, "iştahsızlık": 0.78,
            "yorgunluk": 0.72, "baş_ağrısı": 0.58, "şişmiş_lenf": 0.48,
        },
        "prior": 0.05,
        "color": "#e91e63",
    },
    "Mononükleoz": {
        "short": "Mono",
        "description": "Epstein-Barr virüsü kaynaklı; 'öpücük hastalığı' olarak bilinir.",
        "symptoms": {
            "şişmiş_lenf": 0.90, "boğaz_ağrısı": 0.88, "yorgunluk": 0.85,
            "ateş": 0.82, "baş_ağrısı": 0.65, "iştahsızlık": 0.70,
            "gece_terlemesi": 0.55, "sarılık": 0.38,
        },
        "prior": 0.04,
        "color": "#ff5722",
    },
    "Gıda Zehirlenmesi": {
        "short": "Gıda Zeh.",
        "description": "Kontamine gıda tüketimi sonucu akut gastrointestinal hastalık.",
        "symptoms": {
            "bulantı": 0.92, "kusma": 0.88, "ishal": 0.85,
            "karın_ağrısı": 0.82, "ateş": 0.62, "baş_ağrısı": 0.48,
            "yorgunluk": 0.58,
        },
        "prior": 0.06,
        "color": "#795548",
    },
}

DISEASE_NAMES = list(DISEASES.keys())
