# Deployment Report – Instacart Reorder Prediction  

1 Aralık 2025

---

## 1. Giriş

Bu rapor, Instacart Reorder Prediction projesinin geliştirme ortamından üretim ortamına nasıl taşındığını ve modelin kullanıcıya sunulabilir hale gelmesini sağlayan dağıtım (deployment) adımlarını özetlemektedir.

Model; eğitim sonrası kaydedilen LightGBM ağırlıkları, eşik değeri ve özellik listesi kullanılarak Docker tabanlı bir yapı içinde Hugging Face Spaces üzerinde çalıştırılmaktadır. Arayüz ise Streamlit ile tasarlandı.

---

## 2. Deployment Mimarisi

1. **Model Katmanı**  
   - `lgb_model_final.pkl` dosyasında saklanan LightGBM modeli  
   - `feature_names.json` ile modelin beklentisi olan özellik sırası  
   - `best_threshold.txt` ile karar mekanizması

2. **Uygulama Katmanı**  
   - `src/inference.py` - Model yükleme & tahmin fonksiyonları  
   - `src/app_streamlit.py` - Kullanıcı arayüzü  
   - `src/service_api.py` - Opsiyonel FastAPI entegrasyonu

3. **Dağıtım Katmanı**  
   - Docker   
   - Hugging Face Spaces  
   - GitHub Actions ile otomatik güncelleme

---

## 3. Hugging Face Spaces Deployment

### 3.1 Çalışma Mantığı  
1. Kullanıcı arayüzü Streamlit ile sunulur.  
2. Docker, tüm bağımlılıkları tek bir imajda toplar.  
3. HF Spaces, `Dockerfile`’ı kullanarak uygulamayı otomatik olarak başlatır.

### 3.2 Kullanılan Dosyalar  
- `Dockerfile`  
- `requirements.txt`  
- `src/app_streamlit.py`  
- `models/` altındaki model dosyaları  

### 3.3 Production URL  

**https://huggingface.co/spaces/4F71/instacart-reorder-prediction**

---

## 4. CI/CD Süreci 

Dağıtım sürecini otomatik hale getirmek için GitHub Actions yapılandırılmıştır.

- Her commit sonrası model ve uygulama HF Spaces’e senkronize edilir  
- Deploy hataları anında terminal çıktısında görünür  
- Kod değişiklikleri export edilmeden önce format kontrolünden geçer  
- `.github/workflows/huggingface_sync.yaml`  
- HF API token üzerinden kimlik doğrulaması  
- Otomatik Docker build & push  
- Otomatik Space güncellemesi

---

## 6. Karşılaşılan Sorunlar ve Çözümler

### Git LFS Yapılandırma Hatası  
Model dosyaları büyük olduğu için HF Spaces tarafından algılanmadı.  
**Çözüm:** Git LFS entegre edildi ve model dosyaları doğru formatta depolandı.

### Token Doğrulama Hatası  
GitHub Actions üzerinde HF token tanınmadı.  
**Çözüm:** Secrets - `HF_TOKEN` yeniden oluşturulup doğru biçimde eklendi.

### Docker Çalışma Modu Algılanmadı  
Space, uygulamanın Docker tabanlı olduğunu algılamadı.  
**Çözüm:** README başına HF Docker metadata bloğu eklendi.

---

## 7. Monitoring Sistemi

Model tahminlerinin izlenebilmesi için bir monitoring bileşeni geliştirilmiştir. Her tahmin, lokal bir SQLite veritabanına (`monitoring/predictions.db`) kaydedilir. Kayıtlarda tahmin zamanı, olasılık değeri, eşik bilgisi ve varsa kullanıcı/ürün kimlikleri bulunur.

Tahmin işlemi sonrası loglama şu yapı ile tetiklenir:

```
log_prediction(features, probability, is_reorder, threshold)
```

Loglanan tahminler, Streamlit tabanlı basit bir dashboard ile görselleştirilebilir. Dashboard aşağıdaki komutla çalıştırılır:

```
streamlit run monitoring/dashboard.py
```

Bu ekran; toplam tahmin sayısı, pozitif oran ve olasılık dağılımını gösterir. Monitoring bileşeni lokal kullanım içindir ve üretim ortamına deploy edilmez.

**Dashboard Genel Görünüm ve Detayları**

![Dashboard Overview](../figures/monitoring/monitoring_dashboard_overview.png)
![Dashboard Details](../figures/monitoring/monitoring_dashboard_details.png)

---

## 8. Sonuç

Deployment süreci, modelin yalnızca eğitim odaklı değil; son kullanıcıya erişilebilir şekilde yayınlanabilir bir ürün olmasını sağlamıştır. Docker, HF Spaces ve CI/CD entegrasyonu sayesinde model;

- Tek komutla çalışır,  
- Tutarlı bir şekilde paketlenir,  
- Güncellemeler otomatik olarak canlı ortama aktarılır.

---
 
