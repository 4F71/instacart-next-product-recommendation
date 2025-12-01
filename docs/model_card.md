# Model Card – Instacart Reorder Prediction (v1.0)

1 Aralık 2025

## Model Amacı
Bu model, Instacart kullanıcılarının geçmiş sipariş davranışlarına göre bir ürünün bir sonraki siparişte tekrar alınıp alınmayacağını tahmin eder. Ürün öneri sistemleri, kampanya hedefleme ve stok planlama süreçlerinde kullanılabilir.

---

## Kullanılan Veri
- Veri seti: Instacart Market Basket Analysis  
- 3.4M sipariş, 32M ürün hareketi, 200K kullanıcı  
- Kullanılan özellikler: Kullanıcı alışkanlıkları, ürün popülerliği, kullanıcı–ürün etkileşimi, kategori yoğunlukları  
- Toplam özellik sayısı: **37**  
- Hedef değişken: `reordered` (0/1)

---

## Model
- Algoritma: **LightGBM Classifier**  
- Validasyon: **User-based GroupKFold**  
- Optimizasyon: Optuna (30 deneme)  
- Eşik değeri (threshold): **0.40**  

---

## Performans (Final)
- **F1 Score:** 0.7779  
- **Recall:** 0.91  
- **Precision:** 0.69  

Görseller:  
- `figures/confusion_matrix_final.png`  
- `figures/feature_importance_final.png`  
- `figures/shap_summary_plot.png`

---

## Model Dosyaları
- `lgb_model_final.pkl` – Eğitilmiş model  
- `feature_names.json` – Kullanılan özellik listesi  
- `best_threshold.txt` – Optimal threshold  

---

## Kullanım (Inference)
```python
from src.inference import load_model, predict_single

model, features = load_model()
predict_single(row, model, features)
```

---

Bu model kartı, modelin amacı, veri kaynağı, performansı ve kullanım şeklini özetlemek için hazırlanmıştır.

```
