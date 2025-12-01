# Final Proje Raporu  
    
1 Aralık 2025

---

## 1. Giriş

Bu proje, Instacart kullanıcılarının geçmiş sipariş davranışlarını inceleyerek bir ürünün bir sonraki siparişte tekrar alınıp alınmayacağını tahmin etmeyi amaçlamaktadır. Tekrar satın alma davranışı; ürün öneri sistemleri, kampanya hedefleme ve stok planlama gibi e-ticaret süreçleri için önemli bir göstergedir.

Proje, veri keşfi ile başlayıp modelin üretim ortamına alınmasına kadar uzanan uçtan uca bir makine öğrenimi akışını kapsamaktadır.

---

## 2. Veri Seti

Instacart Market Basket Analysis veri seti: 

**Özet bilgiler:**

- 3.4 milyon sipariş  
- 32 milyon ürün hareketi  
- 200 bin kullanıcı  
- 134 bin benzersiz ürün  
- Zaman, ürün, kullanıcı ve kategori seviyesinde detay

Bu veri seti: kullanıcı alışkanlıklarını ve ürün davranışlarını anladığım en büyük veri setlerinden birisidir.

Detaylı teknik dokümantasyon:  

**`docs/problem_definition.md`**

---

## 3. Keşifsel Veri Analizi (EDA)

Veri keşfi sırasında sipariş zamanları, kategori yoğunlukları ve tekrar satın alma davranışlarını detaylıca inceledim: 

**Öne çıkan bulgular:**

- Sipariş yoğunluğu 10:00–16:00 arasında yükselmektedir.  
- En yoğun günler Pazar ve Pazartesi’dir.  
- Sipariş aralıkları çoğunlukla 3–10 gün civarındadır.  
- En çok sipariş edilen kategori taze meyve–sebzedir.  
- `reordered` oranı yaklaşık %60 seviyesindedir.

Detaylı teknik dokümantasyon:  

**`docs/eda_report.md`**
---

## 4. Baseline Model

İlk referans modeli, yalnızca ürünün genel tekrar satın alma oranını temsil eden `reorder_ratio` özelliği ile oluşturduğum bir Logistic Regression modelidir.

**Baseline sonuçları:**

- F1 Score: 0.7452  
- Recall: 0.8535  
- Precision: 0.6614  

Detaylı teknik dokümantasyon:  

**`docs/baseline_report.md`**

---

## 5. Feature Engineering

EDA’da tespit edilen kullanıcı ve ürün davranışlarını tutarlı şekilde modele öğretebilmek için toplam **37 özellik** üretilmiştir.

**Özellik grupları:**

- Kullanıcı alışveriş ritimleri  
- Zamanlama alışkanlıkları  
- Ürün popülerliği ve tekrar alma oranları  
- Aisle ve departman düzeyinde alışveriş yoğunluğu  
- Kullanıcı–ürün geçmiş ilişkisi  
- Sepet içi pozisyon davranışları  
- Keşif eğilimi

Bu özellikler model performansında belirleyicidir.

Detaylı teknik dokümantasyon:  

**`docs/feature_engineering_report.md`**

---

## 6. Model Eğitimi

Modellemeye başlamadan önce veri seti için en doğru olan modeli keşfetmek için farklı algoritmalar benchmark edilmiştir.

**Varsayılan Ayarlar Benchmark:**

- Logistic Regression - 0.7446  
- XGBoost - 0.7658  
- LightGBM - **0.7663**

LightGBM hızı, bellek verimliliği ve tabular veri uyumu nedeniyle tercih edilip optimize edilmiştir.

### Validasyon Stratejisi

- **User-based GroupKFold**  
- Veri sızıntısı olmaması için aynı kullanıcının hem eğitim hem test setinde bulunması engellenmiştir.

### Optuna Optimizasyonu

- 30 deneme  
- Düşük öğrenme oranı  
- Daha iyi genelleme performansı

### Veri Sızıntısı Kontrolü

- Hedef bilgisiyle doğrudan ilişkili bazı kullanıcı–ürün geçmiş özellikleri kaldırılmıştır.

Detaylı teknik dokümantasyon:  

**`docs/training_report.md`**

---

## 7. Değerlendirme Sonuçları

**Optimal Threshold:** 0.40

**Final performans:**

- F1 Score: **0.7779**  
- Recall: **0.91**  
- Precision: **0.69**

Model performansı baseline modele kıyasla anlamlı bir öğrenme gösterdi.

Model davranışı SHAP analizleriyle incelendiğinde, kullanıcı tekrar alışkanlıkları ve ürünün genel popülerliğinin en güçlü belirleyiciler olduğu görülmektedir.

Detaylı teknik dokümantasyon:  

**`docs/evaluation_report.md`**
**`docs/model_card.md`**

---

## 8. Deployment

Model, Docker tabanlı bir yapı ile paketlenmiş ve Streamlit arayüzü üzerinden erişilebilir hale getirilmiştir.  
CI/CD süreci GitHub Actions ile otomatik olarak çalışmaktadır.

**Canlı demo:** 

https://huggingface.co/spaces/4F71/instacart-reorder-prediction


Detaylı teknik dokümantasyon:  

**`docs/modeployment_reportdel_card.md`**

**Monitoring** 

Modelin tahmin performansının izlenebilmesi için lokal bir monitoring bileşeni geliştirilmiştir. Tahmin edilen her örnek, SQLite tabanlı küçük bir veritabanına (monitoring/predictions.db) kaydedilir. Kayıtlarda tahmin zamanı, olasılık değeri, eşik bilgisi ve sınıf tahmini bulunur.

Kaydedilen bu tahminler, Streamlit tabanlı bir dashboard aracılığıyla görselleştirilebilir. Dashboard; toplam tahmin sayısı, pozitif tahmin oranı ve olasılık dağılımı gibi temel metrikleri gösterir. Bu yapı, modelin üretim sonrasındaki davranışının izlenmesi açısından faydalı bir geliştirme ortamı sağlar.

Dashboard şu komutla başlatılabilir:

```
streamlit run monitoring/dashboard.py
```
**Not:** Monitoring bileşeni yalnızca lokal geliştirme ve analiz amaçlıdır; Hugging Face Spaces üzerinde deploy edilmez.

## 9. Sonuç

Bu projeyle: veri keşfinden üretim ortamına ve dağıtıma kadar tüm adımları içeren uçtan uca bir makine öğrenimi sürecini tamamladım.  

Kullanıcı davranışlarını yansıtan özellikler, doğru validasyon yaklaşımı ve optimizasyon çalışmaları ile yüksek performanslı bir model elde ettim.  
Model, e-ticaret alanında tekrar satın alma davranışını tahmin etmek için uygulanabilir bir çözüm sunmaktadır.

---

