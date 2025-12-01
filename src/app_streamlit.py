import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="Instacart Reorder Prediction",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("Instacart Yeniden Sipariş Tahmin Uygulaması")
st.markdown("""
Bu arayüz, belirli bir **kullanıcı–ürün çifti** için bir sonraki siparişte bu ürünün yeniden alınma olasılığını tahmin eder.
Model çıktısı, arka planda çalışan **LightGBM** algoritması ve optimize edilmiş eşik değerine (Threshold) dayanmaktadır.
""")

with st.expander("Model çıktısı ve Karar Mekanizması hakkında bilgi"):
    st.markdown("""
    * **Model:** LightGBM tabanlı sınıflandırıcı.
    * **Tahmin:** 0 ile 1 arasında bir olasılık değeri üretir.
    * **Eşik Değer (Threshold):** Optimize edilmiş bu değerin üzerindeki olasılıklar **1 (Alınır)**, altındakiler **0 (Alınmaz)** olarak sınıflandırılır.
    * **Margin:** Olasılık ile Eşik arasındaki fark, kararın güven aralığını gösterir.
    """)

st.markdown("---")

st.sidebar.header("Girdi Yöntemi")
mode = st.sidebar.radio("Seçiniz:", ["Manuel Giriş", "Kullanıcı Seçimi (Demo)"])

def get_prediction(features):
    try:
        resp = requests.post(f"{API_URL}/predict", json={"features": features})
        if resp.status_code == 200:
            return resp.json()
        else:
            st.error(f"API Hatası: {resp.text}")
            return None
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

def display_decision_analysis(probability, threshold, is_reorder):
    """Karar analizi, görsel düzeltmeler ve iş yorumu"""
    margin = probability - threshold
    
    st.subheader("Model Karar Analizi")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Modelin Verdiği Olasılık", f"%{probability*100:.1f}")
    col2.metric("Karar Eşiği (Threshold)", f"{threshold:.2f}")
    
    if margin > 0:
        col3.metric("Güven Marjı", f"+{margin:.2f}", delta_color="normal")
    else:
        col3.metric("Güven Marjı", f"{margin:.2f}", delta_color="inverse")
    
    st.markdown("---")
    
    if is_reorder == 1:
        confidence = "YÜKSEK" if probability > 0.70 else "ORTA"
        
        st.success(f"### Tahmin: Ürün Sepete Eklenecek ({confidence} Güven)")
        
        st.info(f"""
        **Neden bu karar verildi?**
        Model, **%{(probability*100):.1f}** olasılıkla bu kullanıcının bu ürünü tekrar alacağını öngördü.
        
        Bu skor, belirlediğimiz **{threshold:.2f}** eşik değerini aştığı için sistem **Pozitif (1)** kararı üretti.
        
        **Olası Sebepler:**
        * Kullanıcının geçmişte bu ürünü (veya benzer kategoriyi) sık alması.
        * Ürünün genel popülaritesinin (Reorder Rate) yüksek olması.
        * Kullanıcının sipariş döngüsünün (Gün aralığı) bu ürünün tüketim süresine uyması.
        """)
        
    else:
        st.error(f"### Tahmin: Ürün Sepete Eklenmeyecek")
        
        st.warning(f"""
        **Neden bu karar verildi?**
        Modelin ürettiği olasılık (**%{probability*100:.1f}**), karar eşiği olan **{threshold:.2f}** değerinin altında kaldı.
        
        **Olası Sebepler:**
        * Kullanıcı daha önce bu ürünü denemiş ama sadık kalmamış olabilir.
        * Kullanıcı "Kaşif" (Yeni ürün denemeyi seven) modunda olabilir.
        * Ürün, kullanıcının rutin alışveriş listesinde henüz yer etmemiş.
        """)


if mode == "Kullanıcı Seçimi (Demo)":
    st.subheader("Gerçek Kullanıcı Senaryosu")
    st.markdown("Bu modda, demo verisetinden rastgele seçilmiş gerçek kullanıcı profilleri üzerinde tahminleme yapılır.")
    
    try:
        users_resp = requests.get(f"{API_URL}/demo_users")
        if users_resp.status_code == 200:
            users = users_resp.json()
            
            if users:
                selected_user = st.selectbox("Analiz Edilecek Kullanıcı ID:", users)
                
                if st.button("Kullanıcı Verilerini Getir ve Tahmin Et"):
                    data_resp = requests.get(f"{API_URL}/get_user_data/{selected_user}")
                    
                    if data_resp.status_code == 200:
                        data = data_resp.json()
                        features = data['features']
                        product_id = data.get('product_id', 'Bilinmiyor')
                        
                        st.write(f"**İncelenen Ürün ID:** `{product_id}`")
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("### Müşteri Profili")
                            user_feats = {k:v for k,v in features.items() if k.startswith('user')}
                            st.dataframe(pd.DataFrame([user_feats]).T.rename(columns={0:'Değer'}), height=300)
                            
                        with c2:
                            st.markdown("### Ürün & Kategori Metrikleri")
                            prod_feats = {k:v for k,v in features.items() if not k.startswith('user')}
                            st.dataframe(pd.DataFrame([prod_feats]).T.rename(columns={0:'Değer'}), height=300)
                        
                        st.markdown("---")
                        
                        result = get_prediction(features)
                        if result:
                            display_decision_analysis(
                                result['probability'], 
                                result['threshold'], 
                                result['is_reorder']
                            )
            else:
                st.warning("Demo verisi bulunamadı. Lütfen 'src/config.py' içindeki demo veri yolunu kontrol edin.")
        else:
            st.error("Kullanıcı listesi API'den alınamadı.")
            
    except Exception as e:
        st.error(f"Sistem Hatası: {e}")


elif mode == "Manuel Giriş":
    st.subheader("Parametre Simülasyonu")
    st.markdown("Bu modda, özellik değerlerini manuel olarak değiştirerek modelin hassasiyetini test edebilirsiniz.")
    
    features = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Müşteri Davranışı")
        features["user_exploration_score"] = st.number_input(
            "Kullanıcı Keşif Skoru (0-1)", value=0.40, step=0.05,
            help="Kullanıcının yeni ürün deneme eğilimi."
        )
        features["user_reorder_ratio"] = st.number_input(
            "Genel Yeniden Sipariş Oranı", value=0.55, step=0.05,
            help="Kullanıcının geçmiş siparişlerindeki reorder oranı."
        )
        features["user_total_orders"] = st.number_input(
            "Toplam Sipariş Sayısı", value=20.0, step=1.0
        )
        features["user_avg_days_between_orders"] = st.number_input(
            "Sipariş Aralığı (Gün)", value=7.0, step=1.0
        )

    with col2:
        st.markdown("### Ürün İstatistikleri")
        features["product_reorder_rate"] = st.number_input(
            "Ürün Reorder Oranı", value=0.50, step=0.05,
            help="Bu ürünün genel kitlesi tarafından tekrar alınma oranı."
        )
        features["product_avg_cart_position"] = st.number_input(
            "Ortalama Sepet Sırası", value=5.0, step=1.0
        )
        features["product_order_count"] = st.number_input(
            "Ürün Toplam Sipariş", value=100.0, step=10.0
        )
        features["aisle_reorder_rate"] = st.number_input(
            "Kategori (Aisle) Reorder Oranı", value=0.30, step=0.05
        )

    if st.button("Simülasyonu Başlat"):
        result = get_prediction(features)
        if result:
            st.markdown("---")
            display_decision_analysis(
                result['probability'], 
                result['threshold'], 
                result['is_reorder'] 
            )