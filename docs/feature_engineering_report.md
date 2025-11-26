# Feature Engineering Raporu 

26 Kasım 2025

Feature Engineering'de kullanıcı, ürün ve sipariş davranışlarını analiz ederek modelin anlayabileceği yapısal sinyallere dönüştürdüm.  
EDA ve Baseline süreçlerindeki analizlerim & yorumlamalarım ve kaggle top solutions'dan ilham alınarak toplam **37 güçlü feature** ürettim..

---


## 1) Kullanıcı Özellikleri (User Features)

Kullanıcıların alışveriş düzeni, sepet davranışı ve sadakat eğilimlerini temsil eden özellikler oluşturuldu.  
Bu gruptaki sinyaller:

- Toplam sipariş sayısı  
- Yeni kullanıcı / deneyimli kullanıcı ayrımı  
- Sipariş zamanı tercihleri (gün, saat, hafta sonu, peak saatler)  
- Ortalama sipariş aralığı ve en uzun boşluk  
- Haftalık / aylık alışveriş alışkanlığı  
- Genel reorder oranı  
- Yeni ürün keşfetme eğilimi (exploration score)

Bu özellikler, kullanıcıyı hem alışkanlık hem davranış açısından modelin anlamasını sağlayacak.

---

## 2) Ürün Özellikleri (Product Features)

Bir ürünün popülerliğini, yeniden satın alınma potansiyelini ve pazardaki konumunu temsil eden sinyaller çıkarıldı:

- Ürün toplam sipariş sayısı  
- Reorder oranı (temel ihtiyaç ürünü sinyali)  
- Farklı kullanıcı sayısı (ürün yaygınlığı)  
- Sepetteki ortalama konumu  
- Organic ürün olup olmadığı  
- Departman ve aisle popülerliği

Bu sinyaller ürünün “temel alışveriş mi, dönemsel mi” olduğunu modelin anlaması içindir.

---

## 3) Kategori Bazlı Özellikler (Aisle & Department Features)

Market mimarisi seviyesinde kategori davranışlarını modele anlatmak için:

- Koridordaki toplam sipariş hacmi  
- Departman toplam sipariş hacmi  
- Ürün çeşitliliği  
- Kullanıcı bazlı favori koridor/departman  
- Kategori çeşitliliği

Kullanıcıların belirli kategorilere bağlılık gösterdiği, EDA’da güçlü şekilde gözlemledim. Gözlemlerim sonucunda FE’ye dönüştürdüm.

---

## 4) Kullanıcı–Ürün Etkileşimleri (User–Product Interaction)

Bu aşama, tüm top solution modellerinde kritik rol oynayan sinyalleri kapsar.  
Bir kullanıcının belirli bir ürüne olan ilişki gücünü ifade eder:

- Ürünü kaç kez aldığı  
- En son hangi siparişte aldığı  
- Son alımdan sonra kaç sipariş geçtiği  
- Kullanıcı içi ürün satın alma oranı  
- Kullanıcı–ürün bazlı reorder davranışı  
- Sepet içi konum alışkanlığı

Modelin “kime ne önerilir?” sorusunu doğru cevaplayabilmesi için bu grup önemli.

---

## 5) Genel Değerlendirme

Feature Engineering süreci, EDA’da gözlenen örüntüleri gerçek sinyallere dönüştürerek modelin karar alanını zenginleştirdi.  
Toplam 37 feature üretildi ve kaydedildi. Üretilen FE'ler sayesinde kullanıcı–ürün etkileşimleri dahil tüm davranış yapısı modele aktarılacak hale geldi.

Bu aşama ile birlikte model eğitimine geçmek için gerekilen adımlar tamamlanmıştır.

---

Feature Engineering tamamlandı.
Bir sonraki aşama: **Model Training**

