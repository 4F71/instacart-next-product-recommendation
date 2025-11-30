# -*- coding: utf-8 -*-
"""
inference.py
---
model yükleme-veri hazırlama- ve tahminleme mekanizmasıdır
"""


from typing import Dict, List, Tuple

import joblib
import numpy as np

from .config import MODEL_PATH, load_feature_list, load_threshold


class ReorderModel:
    
    def __init__(self) -> None:
        """
        config.py dosyasına tanımladığım  yolları kullanarak: 
        lgb_model_final.pkl + feature_names.json + best_threshold.txt yüklemeyi yapıyoruz.
        """
        self.model = joblib.load(MODEL_PATH)
        self.feature_list: List[str] = load_feature_list()
        self.threshold: float = load_threshold()

    def _to_array(self, features: Dict[str, float]) -> np.ndarray:
        """
        modelin isteyeceği şekilde numpy vektörüne dönüştürüp
        eksik featureler varsa 0.0 değerini hata çıkmaması için ekliyoruz.
        """
        values = [float(features.get(col, 0.0)) for col in self.feature_list]
        return np.array([values], dtype=float)

    def predict_proba(self, features: Dict[str, float]) -> float:
        x = self._to_array(features)
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(x)[0, 1]
        else:
            proba = self.model.predict(x)[0]
        return float(proba)


    def predict_label(self, proba: float) -> int: 
        return int(proba >= self.threshold)

    def predict(self, features: Dict[str, float]) -> Tuple[float, int]:
        """
        deploy kısmında asıl çağıracağım fonksiyon
        """
        proba = self.predict_proba(features)
        label = self.predict_label(proba)
        return proba, label



reorder_model = ReorderModel()
