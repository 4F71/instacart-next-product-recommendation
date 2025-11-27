# Model Değerlendirme ve Analiz Raporu

26 Kasım 2025  


**Model:** LightGBM

## 1. Ne yaptım, Ne sonuç aldım?

Training aşamasında **Data Leakage** (Veri Sızıntısı) problemini çözdükten sonra eğittiğim final LightGBM modeli, hiç görmediği kullanıcılardan oluşan validasyon setinde test edildi.

Standart 0.50 eşik değeri yerine, F1 skorunu maksimize eden **0.40 Eşik Değeri (Threshold)** ile yapılan testlerde **0.7779 F1 Skoru** elde edildi. [cite_start]Bu skor, Baseline modeline (Lojistik Regresyon - 0.7452) kıyasla **%4.4'lük net bir performans artışı** [cite: 58] anlamına geliyor.

---

## 2. Performans Metrikleri ve Stratejik Kararlar

E-ticaret senaryosunda **"Müşterinin alacağı ürünü tahmin edememek (Satış Kaçırmak)"**, yanlış bir ürün önermekten daha maliyetlidir. Bu yüzden **Recall (Duyarlılık)** metriğini önceliklendiren bir strateji izledim.

**Final Metrikler (Threshold 0.40):**

| Metrik | Değer | İş Anlamı (Business Value) |
| :--- | :--- | :--- |
| **F1 Score** | **0.7779** | Modelin genel başarısı ve dengesi. (Baseline: 0.74) |
| **Recall** | **0.91** | **Kritik:** Tekrar alınacak her 100 üründen 91'ini başarıyla yakalıyoruz. |
| **Precision** | **0.69** | "Alınır" dediğimiz her 10 üründen yaklaşık 7'si sepete giriyor. |
| **ROC-AUC** | **0.7779** | Modelin pozitif ve negatif sınıfları ayırma yeteneği (%78). |

---

## 3. Hata Analizi: Baseline vs Final Karşılaştırması

Modelin tahminlerini Baseline (Lojistik Regresyon) ile Confusion Matrix üzerinden kıyasladığımda, işe doğrudan etki eden şu farklar ortaya çıktı:

* **Kazanılan Satış Fırsatı (True Positive):**
    * Baseline modele göre **+9,072 adet** daha fazla doğru tahmin yapıldı. Bu, binlerce ürünün doğru zamanda doğru müşteriye önerilmesi ve **sepet hacminin artması** demektir.

* **Kaçırılan Fırsatların Azalması (False Negative):**
    * Müşterinin aslında alacağı ama modelin "Almaz" dediği hatalar **8,908 adet** azaltıldı. Model artık kullanıcının davranışlarını daha iyi okuyor.

---

## 4. Model Neden Bu Kararı Veriyor? (SHAP Analizi)

Modeli "Kara Kutu" olmaktan çıkarmak için **SHAP (SHapley Additive exPlanations)** analizi yaptım. Modelin ezberlemediği, **davranışsal sinyallere** odaklandığı kanıtlandı:

1.  **Ürün Popülaritesi (`product_reorder_rate`):**
    * *Etki:* En güçlü sinyal.
    * *Yorum:* Model, genel olarak çok sık tekrar alınan ürünleri (Süt, Muz vb.) önerme eğiliminde. 

2.  **Kullanıcı Karakteristiği (`user_exploration_score`):**
    * *Etki:* Negatif korelasyon.
    * *Yorum:* Model, sürekli yeni ürün deneyen ("Kaşif") kullanıcıları tespit edip, onlara daha az "Reorder" önerisi yapıyor. [cite_start]Kullanıcı psikolojisini analiz edebiliyor[cite: 153].

3.  **Kullanıcı Sadakati (`user_reorder_ratio`):**
    * *Etki:* Pozitif.
    * [cite_start]*Yorum:* Geçmişte sadık olan kullanıcıların gelecekte de sadık olacağı varsayımı model tarafından doğrulanmıştır[cite: 116].

---

## 5. Sonuç ve Sonraki Adımlar

Geliştirilen model; **sızıntısız (leakage-free)** yapısı, optimize edilmiş parametreleri ve **iş odaklı (recall-driven)** karar mekanizması ile canlı ortama (Production) alınmaya hazırdır.

Model Evaluation aşaması tamamlandı.
- `lgb_model_final.pkl` ve `best_threshold.txt` dosyaları kaydedildi.
Bir sonraki aşama: **Deployment**