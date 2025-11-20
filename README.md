# Instacart Next Product Recommendation (Uçtan Uca ML Projesi)

Bu repo, Zero2End Machine Learning Bootcamp kapsamında geliştirdiğim
uçtan uca makine öğrenimi projesinin çalışma alanıdır.

**Projenin ana amacı:** Instacart Market Basket Analysis datasını kullanarak  
kullanıcıların bir sonraki satın alacağı ürünleri tahmin edebilen,  
üretim seviyesine taşınabilir bir ML sistemi geliştirmek.

---

## 📦 Dataset

**Instacart Market Basket Analysis**  
https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis

- 3.4M+ sipariş  
- 200K+ kullanıcı  
- 50K unique ürün  
- Gerçek kullanıcı davranışları: zamanlama, departman, kategori ve “reorder” bilgisi

---

## 📁 Proje Yapısı

instacart-next-product-recommendation/
│
├── data/
│ ├── raw/ # Kaggle CSV dosyaları
│ ├── processed/ # Eğitime hazır temiz veri
│ └── interim/ # Feature engineering sırasında üretilen ara veri
│
├── notebooks/ # EDA, modelleme ve analiz notebook'ları
├── src/ # Modüler ML pipeline kaynak kodları
├── api/ # FastAPI test uygulaması / inference servisi
├── docs/ # Proje dokümanları
├── models/ # Eğitilmiş modeller ve artefact'lar
├── tests/ # Unit test dosyaları
│
└── README.md

---

## 🚧 Proje Durumu

Proje geliştirme aşamasındadır.  
EDA, feature engineering ve modelleme ilerledikçe README güncellenecektir.

---
