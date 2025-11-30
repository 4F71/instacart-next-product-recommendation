# -*- coding: utf-8 -*-
"""
Config.py
---
projenin tüm dosya yollarını tek bir yerdeen konrol etmek için hazırlanmıştır.
proje'nin sürdürülebilirliği açısından SRC yapı sistemi tercih edilmiştir.

"""

from pathlib import Path
import json

# Ana dizin 
SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

# Model klasörü
MODELS_DIR = ROOT_DIR / "models"

# Dosya yolları 
MODEL_PATH = MODELS_DIR / "lgb_model_final.pkl"
FEATURE_LIST_PATH = MODELS_DIR / "feature_names.json"
THRESHOLD_PATH = MODELS_DIR / "best_threshold.txt"


def load_feature_list():
    if FEATURE_LIST_PATH.exists():
        with open(FEATURE_LIST_PATH, "r") as f:
            return json.load(f)
    return []


def load_threshold(default: float = 0.40) -> float:
    if THRESHOLD_PATH.exists():
        text = THRESHOLD_PATH.read_text().strip()
        try:
            return float(text)
        except ValueError:
            return default
    return default