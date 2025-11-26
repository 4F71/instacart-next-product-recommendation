# Model Training Raporu

26 Kasım 2025

## 1. Yönetici Özeti (Executive Summary)

Bu aşamada, Feature Engineering sürecinde üretilen özellikler kullanılarak, problemi en iyi çözen algoritma belirlenmiş ve optimize edilmiştir. Süreç sırasında tespit edilen **kritik veri sızıntısı (Data Leakage)** problemi, kök neden analizi ile giderilmiş ve modelin gerçek hayat performansını yansıtan **0.7779 F1 Skoru** elde edilmiştir. Bu skor, Baseline modeline (0.7452) kıyasla **%4.4'lük net bir performans artışı** sağlamıştır.

---

## 2. Metodoloji ve Stratejik Kararlar

Model eğitim stratejisi, önceki aşamalardaki (EDA ve Baseline) bulgulara dayanarak şu şekilde kurgulanmıştır:

### 2.1. Validasyon Stratejisi: User-Based GroupKFold

* **EDA Raporu:** EDA sürecinde kullanıcıların %60'a varan sadakat oranına ve 7-30 günlük düzenli alışveriş döngülerine sahip olduğu tespit edilmişti.
* **Karar:** Standart `Random Split` yerine `User-based GroupKFold` kullandım.
* **Gerekçe:** Bir kullanıcının siparişlerini eğitim ve test setlerine dağıtmak, modelin kullanıcının karakterini ezberlemesine (Overfitting) neden olacaktı. Kullanıcı bazlı ayrım ile modelin hiç görmediği kullanıcılardaki performansı simüle edildi.

### 2.2. Model Seçimi (Benchmark)

Aday modeller aynı validasyon setinde, varsayılan parametrelerle karşılaştırıldı:
* **Logistic Regression:** 0.7446
* **LightGBM:** 0.7663
* **XGBoost:** 0.7658

* **Seçim:** Hız, bellek verimliliği ve en yüksek skoru vermesi nedeniyle **LightGBM** seçildi.


### 2.3. Memory Optimization

* **Sorun:** 1.38 milyon satır ve 37 değişkenli veri seti, varsayılan veri tipleriyle (`float64`) belleği (RAM) aşırı zorluyodu.
* **Çözüm:** Veri yükleme aşamasında `reduce_mem_usage` ile sayısal veriler, veri kaybı olmayacak en küçük tipe (`float32`, `int8` vb.) dönüştürdüm.
* **Sonuç:** Bellek kullanımı **%50 oranında düşürüldü.** 
---

## 3. Kritik Olay: Data Leakage Tespiti ve Çözümü

Benchmark sürecinde ağaç tabanlı modellerin **1.0000** F1 skoru üretmesi üzerine analiz başlatıldı.

### 3.1. Teşhis

* **Belirti:** Gerçek dünya verisinde %100 başarı teknik olarak imkansızdır.
* **Analiz:** Modelin *Feature Importance* grafiği incelendiğinde, `up_orders` (Kullanıcı-Ürün Sipariş Sayısı) özelliğinin diğer tüm özelliklerden daha baskın olduğu gördüm.
* **Kök Neden:** Feature Engineering aşamasında bu özellik hesaplanırken, *eğitim setindeki (hedef) siparişin de* sayıma dahil edildiği ve bu sayede modelin cevabı (reordered=1) direkt olarak gördüğü anladım. 

### 3.2. Çözüm

Sızıntıya neden olan ve geleceği ifşa eden aşağıdaki özellikleri eğitim setinden çıkardım:

* `up_orders`
* `up_last_order_number`
* `up_order_rate`
* `up_cart_mean`

**Sonuç:** Temizlik sonrası LightGBM skoru **0.7663** seviyesine oturarak gerçekçi bir zemine kavuştu.

---

## 4. Optimizasyon ve Final Sonuçlar

### 4.1. Hiperparametre Optimizasyonu (Optuna)

30 denemelik Optuna süreci ile `Log Loss` metriği minimize edildi.
* **Seçilen Parametreler:** Düşük öğrenme hızı (`learning_rate: 0.02`) ve orta derinlik (`num_leaves: 83`) ile modelin ezberlemesi engellendi ve genelleme yeteneği artırıldı.

### 4.2. Threshold (Eşik Değeri) Tuning

* **Referans (Baseline Raporu):** Baseline modelde standart 0.50 eşik değeri kullanılmış ve Precision değerinin (0.66) düşük kaldığı gözlemlenmişti.
* **Aksiyon:** Final modelin ürettiği olasılıklar için 0.10 ile 0.60 arasındaki tüm eşik değerleri test edildi.
* **Sonuç:** En yüksek F1 skorunu veren eşik değeri **0.40** olarak belirlendi.

### 4.3. Final Karşılaştırma Tablosu

| Metrik | Baseline Model | Final LightGBM | Fark |
| :--- | :--- | :--- | :--- |
| **Model** | Logistic Regression | LightGBM (Tuned) | - |
| **Feature Sayısı** | 2 (`reorder_ratio`) | 31 (Seçilmiş) | +29 |
| **Threshold** | 0.50 (Sabit) | **0.40 (Optimize)** | - |
| **F1 Score** | 0.7452 | **0.7779** | **+%4.4** |

---


Model Training aşaması tamamlandı. 
- `lgb_model_final.pkl` ve optimize edilen `best_threshold.txt` dosyaları kaydedilmiştir.
Bir sonraki aşama: **Model Evaluation**