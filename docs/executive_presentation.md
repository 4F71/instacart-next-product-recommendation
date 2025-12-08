# Instacart Yeniden Sipariş Tahminleme Sistemi - Üst Yönetim Sunumu

> Not: Bu sunumdaki finansal rakamlar ve oranlar, sistemin potansiyel iş etkisini göstermek amacıyla **senaryo bazlı** olarak kurgulanmıştır. Gerçek ortamda, şirket verileriyle yeniden kalibre edilmesi önerilir.

---

## Proje Özeti

Müşterilerimizin bir sonraki siparişlerinde hangi ürünleri tekrar satın alacağını tahmin eden bir sistem geliştirdik.  
Sistem, 3.4 milyon sipariş ve 32 milyon ürün hareketi verisi üzerinde eğitildi.  
Müşteri alışveriş alışkanlıklarını öğrenerek gelecekteki satın alma davranışlarını tahmin ediyor.

---

## Kritik İş Soruları ve Cevapları

### Soru 1: Bu sistem şirkete finansal olarak ne kazandırabilir?

**Mevcut Durum Varsayımsal Analizi (Örnek Senaryo):**
- Yanlış stok planlaması nedeniyle aylık **~500K TL** seviyesinde kayıp
- Kişiselleştirilmemiş öneriler nedeniyle **%35 sepet terk oranı**
- Verimsiz kampanyalar nedeniyle pazarlama bütçesinin yaklaşık **%12’si boşa harcanıyor**

**Sistem Sonrası Projeksiyonlar (6 Aylık Senaryo):**
- Daha iyi stok planlaması ile **aylık ~300K TL tasarruf**
- Sepet terk oranında **%10’luk azalma** → aylık ~800K TL ek gelir
- Kampanya verimliliğinde **%25’lik iyileşme** → aylık ~150K TL tasarruf

**Örnek Net Finansal Kazanım (Senaryo): Aylık ≈ 1.25M TL, Yıllık ≈ 15M TL**

---

### Soru 2: Hangi departmanlar bu sistemden faydalanacak?

![En Popüler Departmanlar](../figures/departments_top20.png)  
*Rapor Görseli 1: Departman Bazlı Sipariş Dağılımı*

**Pazarlama Departmanı:**
- Kişiselleştirilmiş kampanya tasarımı
- Hedefli promosyon stratejileri
- Müşteri segmentasyonu iyileştirmesi  
**Beklenen fayda (senaryo):** Kampanya dönüşümünde **%20–30 artış**

**Satın Alma ve Stok Yönetimi:**
- Tahmine dayalı sipariş verme
- Sezonsal talep öngörüsü
- Depo alanı ve stok devir hızının optimizasyonu  
**Beklenen fayda:** Fire oranında **%30–40 azalma**

**Müşteri Hizmetleri:**
- Proaktif müşteri iletişimi
- Stok dışı ürün şikayetlerinde azalma
- Müşteri memnuniyeti artışı  
**Beklenen fayda:** Şikayet sayısında **%20–25 düşüş**

---

### Soru 3: Müşteri davranışlarından ne öğrendik?

![Sipariş Aralığı Dağılımı](../figures/orders_days_since_prior.png)  
*Rapor Görseli 2: Müşteri Alışveriş Periyotları*

![Zamansal Sipariş Dağılımı](../figures/orders_temporal_distribution.png)  
*Rapor Görseli 3: Haftalık ve Günlük Sipariş Yoğunlukları*

**Kritik Bulgular:**
- Müşterilerin önemli bir kısmı **düzenli haftalık alışveriş** yapıyor
- Hafta sonları sipariş hacmi belirgin şekilde yükseliyor
- Siparişlerin çoğu **10:00–16:00** arasında veriliyor
- Ortalama sepette ~10 ürün var, **ilk 5 ürün** sepetin omurgasını oluşturuyor

**İş Anlamı:**
- Haftalık stok rotasyonu planlanabilir
- Hafta sonu için lojistik kapasitesi güçlendirilmeli
- Öğlen saatlerine özel kampanyalar anlamlı
- İlk 5 ürüne yönelik öneri kalitesi kritik

---

### Soru 4: En çok hangi ürünler tekrar satın alınıyor?

![En Çok Sipariş Edilen Ürünler](../figures/products_top20.png)  
*Rapor Görseli 4: En Popüler 20 Ürün*

![Sepete Ekleme Sırası](../figures/cart_order_distribution.png)  
*Rapor Görseli 5: Ürünlerin Sepete Eklenme Sırası*

**Ürün İstatistikleri (Veri Üzerinden):**
- Bazı temel ürünler (örneğin muz ve taze ürünler) sipariş hacminde öne çıkıyor
- Taze meyve–sebze kategorisi toplam satışın kayda değer bir bölümünü oluşturuyor
- Sepete ilk eklenen ürünler, sepet içinde yüksek satın alma oranına sahip

**Aksiyon Önerileri:**
- Kritik ürünlerde “stokta bulunabilirlik” önceliklendirilmelidir
- Talebi yüksek kategorilerde ürün çeşitliliği ve stok derinliği dikkatle yönetilmelidir
- “İlk önerilen ürünler” alanı, bu davranışlara göre optimize edilmelidir

---

### Soru 5: Sistemin başarı oranı nedir?

![Model Performans Karşılaştırması](../figures/confusion_matrix_final.png)  
*Rapor Görseli 6: Tahmin Başarı Matrisi*

**Performans Özeti (Validasyon Seti):**
- **Tekrar alınacak ürünlerin %91’i** doğru tahmin ediliyor (Recall = 0.91)
- Önerilen ürünlerin **%69’u gerçekten satın alınıyor** (Precision = 0.69)
- **Genel başarı skoru (F1): 0.7779**

**Ne Anlama Geliyor?**
- 10 üründen yaklaşık 9’unu doğru yakalayan bir yapı --> müşterinin alışkanlıklarını iyi okuyan model
- Yanlış öneri oranı düşük --> daha az hayal kırıklığı, daha az şikayet
- Optimizasyon imkanı olan, öğrenmeye açık bir sistem

---

### Soru 6: Hangi faktörler tahminleri etkiliyor?

![Feature Importance](../figures/feature_importance_final.png)  
*Rapor Görseli 7: Tahmin Faktörleri*

![SHAP Analizi](../figures/shap_summary_plot.png)  
*Rapor Görseli 8: Faktörlerin Detaylı Etkisi*

**En Etkili Faktörler:**
1. Ürünün genel tekrar satın alınma oranı (product_reorder_rate)
2. Müşterinin genel sadakat seviyesi (user_reorder_ratio)
3. Müşterinin yeni ürün deneme eğilimi (exploration score)
4. Toplam sipariş sayısı (müşteri deneyimi)
5. Son alışveriş ile şimdiki sipariş arasındaki süre

**Pratik Kullanım Örnekleri:**
- Yeni müşterilere, yüksek popülerlik ve yüksek tekrar oranına sahip ürünler önerilebilir
- Sadakati yüksek müşterilere “favori ürün” temelli kampanyalar kurgulanabilir
- Uzun süredir alışveriş yapmayan müşterilere hatırlatma iletişimi yapılabilir

---

### Soru 7: Optimal tahmin seviyesi nasıl belirlendi?

![Eşik Değeri Optimizasyonu](../figures/threshold_optimization.png)  
*Rapor Görseli 9: Tahmin Eşiği Optimizasyonu*

**Optimizasyon Stratejisi:**
- Farklı eşik değerleri denenerek F1 skoru ve Recall dengelendi
- “Müşterinin alacağı ürünü kaçırmamak” önceliklendirildi
- Agresif satış yerine güven ve deneyim odaklı yaklaşım tercih edildi

**Sonuç:**
- **%40 (0.40) eşik değeri** en dengeli sonuçları verdi
- Daha az “kaçırılan satış”, kontrollü yanlış öneri oranı
- İş hedefleri ile model çıktıları hizalandı

---

### Soru 8: Sistem nasıl izleniyor ve kontrol ediliyor?

![Monitoring Dashboard Overview](../figures/monitoring/monitoring_dashboard_overview.png)  
*Rapor Görseli 10: Canlı İzleme Paneli*

![Monitoring Dashboard Details](../figures/monitoring/monitoring_dashboard_details.png)  
*Rapor Görseli 11: Detaylı Tahmin Takibi*

**İzleme Kapsamı:**
- Günlük tahmin sayısı
- Pozitif tahmin oranları
- Olasılık dağılımları
- Örnek tahmin kayıtları

**Yönetimsel Fayda:**
- Anlık performans takibi
- Anomali tespiti (model bozulması, veri sorunları)
- Performans düşüşlerinde hızlı müdahale imkanı

---

## Rekabet Avantajı ve Pazar Konumu (Kurgu Perspektif)

### Sektör Karşılaştırması (Senaryo)

**Varsayımsal Durum:**
- Sektörde benzer sistemlerin ortalama F1 skorunun ~0.65 seviyelerinde olduğu kabul edilirse,
- Bizim sistemimiz: **0.7779 F1** ile bu seviyenin belirgin şekilde üzerinde konumlanıyor.

**Rekabet Üstünlüğü:**
- Daha isabetli stok yönetimi
- Daha yüksek müşteri memnuniyeti
- Daha verimli kampanya ve operasyon kurgusu

---

### Müşteri Deneyimi İyileştirmeleri

![Baseline vs Final Model](../figures/baseline_confusion_matrix.png)  
*Rapor Görseli 12: Sistem Öncesi ve Sonrası Karşılaştırma (Baseline vs Final)*

**Önceki Durum (Basit Model / Heuristikler):**
- Görece genel kampanyalar
- Müşteriye özel olmayan öneriler
- Daha yüksek stok maliyetleri

**Yeni Sistem:**
- Otomatik, veri tabanlı tahminler
- Kişiye ve davranışa göre özelleşmiş öneriler
- Daha kontrollü ve verimli stok yönetimi

---

## Yatırım ve Geri Dönüş Analizi (Senaryo Bazlı)

### Maliyet Kırılımı (Örnek Senaryo)

**Geliştirme Maliyeti (Tek Seferlik):**
- Veri altyapısı: 150K TL
- Model geliştirme: 200K TL
- Sistem entegrasyonu: 100K TL
- Test ve optimizasyon: 50K TL  
**Toplam: ~500K TL**

**Yıllık İşletme Maliyeti (Tahmini):**
- Sunucu ve altyapı: 60K TL
- Bakım ve güncelleme: 120K TL  
**Toplam: ~180K TL / yıl**

### Kazanç Projeksiyonu (Senaryo)

**Yıl 1 Örneği:**
- Beklenen toplam ek katkı: **≈ 15M TL**
- Yatırım + İşletme: ≈ 680K TL  
→ **Net Senaryo Karı: ≈ 14.32M TL**  
→ **ROI: ~%2.000+ (senaryosal)**

**3 Yıllık Örnek Projeksiyon:**
- Toplam katkı: ≈ 45M TL
- Toplam maliyet: ≈ 1.04M TL  
→ **Net Kar: ≈ 43.96M TL (senaryo bazlı)**

> Not: Bu hesaplamalar, sistemin etkisini görünür kılmak için oluşturulmuş örnek projeksiyonlardır. Gerçek uygulamada, şirket verileriyle yeniden hesaplanması gerekir.

---

## Risk Değerlendirmesi

### İş Riskleri ve Önlemler (Kurgu)

| Risk                         | Olasılık | Etki  | Önlem / Azaltma Stratejisi                     |
|------------------------------|----------|-------|-----------------------------------------------|
| Müşteri adaptasyon sorunu    | Düşük    | Orta  | Kademeli rollout, A/B test, geri bildirim     |
| Veri gizliliği endişesi      | Düşük    | Yüksek| KVKK uyumu, açık aydınlatma metinleri         |
| Rekabet tepkisi              | Orta     | Düşük | Sürekli iyileştirme, farklılaşan deneyim      |
| Teknik arıza / kesinti       | Düşük    | Orta  | Yedekleme, monitoring, rollback stratejisi    |

### Başarısızlık Senaryosu

**En Kötü Senaryo Örneği:**
- Sistem beklenen performansın sadece %50’sini gösterir
- Yıllık katkı potansiyeli 15M TL yerine ~7.5M TL’de kalır  
Yine de, yatırım ve işletme maliyetlerine göre sistem hala pozitif katkı üreten bir yapıda kalabilir.

---

## Uygulama Planı (Kurgu Yol Haritası)

### Aşama 1: Pilot Uygulama (1. Ay)
- Örnek: İstanbul bölgesinde, müşteri tabanının %10’unda
- Belirli kategori (örneğin taze ürünler) ile başlama
- Günlük performans takibi ve raporlama

### Aşama 2: Genişletme (2–3. Ay)
- 2–3 büyük şehirde, daha geniş kategori seti
- A/B test ile öneri sisteminin etkisinin ölçümü
- Kampanya ve stok tarafında küçük optimizasyonlar

### Aşama 3: Ulusal Yayılım (4–6. Ay)
- Tüm bölgelerde, tüm müşterilerde devreye alma
- Otomatik çalışabilen batch prediction + izleme
- Kademeli iyileştirme döngüleri

---

## Kritik Başarı Faktörleri

### Organizasyonel Gereksinimler

1. **Departmanlar Arası Koordinasyon**
   - Pazarlama, IT, Operasyon ekiplerinin ortak çalışması
   - Haftalık kısa durum toplantıları
   - Ortak KPI seti

2. **Veri Kalitesi**
   - Güncel müşteri ve ürün verisi
   - Tutarlı stok bilgiler
   - Veri kalitesini izleyen süreçler

3. **Teknoloji Altyapısı**
   - Güvenilir sunucular
   - Yeterli işlem gücü
   - Öneri sistemi / kampanya motoru ile entegrasyon

4. **İnsan Kaynağı (Minimum)**
   - 1–2 veri analisti / bilimci
   - 1 sistem / uygulama sorumlusu
   - İş birimi temsilcileri (Pazarlama / Operasyon)

---

## Sonuç ve Öneriler

### Özet

Bu sistem, müşteri alışveriş davranışlarını öğrenerek gelecekteki satın alımları tahmin ediyor.  
Validasyon sonuçlarına göre, **tekrar alınacak ürünlerin büyük kısmını başarıyla yakalayan** bir model performansı elde edildi.  
Kurgulanan senaryolarda, sistemin **yıllık milyon TL seviyesinde ek değer üretme potansiyeli** bulunuyor.

### Neden Şimdi?

1. **Pazar Dinamikleri:** Kişiselleştirilmiş deneyim, e-ticaret için yeni standart haline geliyor.  
2. **Veri Hazırlığı:** Elimizde çok kapsamlı ve kullanıma hazır bir veri seti var.  
3. **Teknik Olgunluk:** Model, pipeline ve monitoring bileşenleri prototip seviyesinde hazır.  
4. **Rekabet:** Veri odaklı çalışan sistemler, fiyat rekabetinin ötesinde avantaj yaratıyor.

### Karar Noktaları

**Onaylanması Gerekenler (Kurgu):**
- Başlangıç yatırımı (~500K TL)  
- Küçük ama net tanımlı bir çekirdek ekip  
- Pilot senaryonun kapsamı (bölge / kategori / süre)

**Zaman Çizelgesi (Örnek):**
- Karar: Bu hafta  
- Pilot başlangıç: 2 hafta içinde  
- İlk sonuçlar: 1 ay içinde  
- Yaygınlaştırma: 6 ay içinde



Sistemin, kontrollü bir pilot uygulama ile gerçek ortamda test edilmesini ve sonuçlara göre kademeli genişletme stratejisinin izlenmesini öneriyoruz.  
Risk yönetilebilir, potansiyel kazanç ise anlamlı seviyede.

