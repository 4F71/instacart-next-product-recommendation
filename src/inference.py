# -*- coding: utf-8 -*-
"""
inference.py
---
model yükleme-veri hazırlama- ve tahminleme mekanizmasıdır
"""

import numpy as np
import joblib
import sys
from pathlib import Path

try:
    from src import config
except ImportError:
    import config

try:
    from monitoring.log import log_prediction
except ImportError:
    log_prediction = None


class InstacartPredictor:
    def __init__(self):
        self.model = None
        self.threshold = 0.40
        self.feature_names = []
        self._load_assets()

    def _load_assets(self):
        if config.MODEL_PATH.exists():
            self.model = joblib.load(config.MODEL_PATH)
        self.threshold = config.load_threshold()
        self.feature_names = config.load_feature_names()

    def predict(self, features):

        if self.model is None:
            return {"error": "Model bulunamadı"}

        cols_to_use = self.feature_names if self.feature_names else list(features.keys())

        input_vector = []
        for col in cols_to_use:
            val = features.get(col, 0.0)
            try:
                val = float(val)
            except (TypeError, ValueError):
                val = 0.0
            input_vector.append(val)

        X_input = np.array(input_vector).reshape(1, -1)

        try:
            if hasattr(self.model, "predict_proba"):
                probability = self.model.predict_proba(X_input)[0][1]
            else:
                probability = self.model.predict(X_input)[0]
        except Exception as e:
            return {"error": str(e)}

        is_reorder = 1 if probability >= self.threshold else 0

        result = {
            "probability": float(probability),
            "is_reorder": is_reorder,
            "threshold": self.threshold
        }

        if log_prediction is not None:
            try:
                log_prediction(features, result["probability"], result["is_reorder"], result["threshold"])
            except Exception:
                pass

        return result
