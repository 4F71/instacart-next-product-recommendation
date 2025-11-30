# -*- coding: utf-8 -*-

import sys
from pathlib import Path
import json

import requests
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.config import load_feature_list


API_URL = "http://localhost:8000/predict"


@st.cache_data
def get_feature_list():
    return load_feature_list()


def render_manual_input(feature_list):
    st.subheader("Müşteri ve Ürün Özellikleri")

    st.markdown(
        """
Bu form, belirli bir **müşteri–ürün çifti** için geçmiş davranışlardan türetilmiş özet metrikleri temsil eder.

- Sol taraftaki alanlar: müşteriye ait alışveriş alışkanlıkları
- Sağ taraftaki alanlar: ilgili ürün ve ait olduğu reyonun istatistikleri
"""
    )

    features = {}

    col_user, col_product = st.columns(2)

    with col_user:
        st.markdown("### Müşteri özellikleri")

        features["user_exploration_score"] = st.number_input(
            "Kullanıcının yeni ürün keşfetme skoru",
            help="0 ile 1 arasında normalize edilmiş skor (ör: 0.40 = orta seviye keşif)",
            value=0.40,
            step=0.05,
            min_value=0.0,
            max_value=1.0,
        )

        features["user_reorder_ratio"] = st.number_input(
            "Kullanıcının genel yeniden sipariş oranı",
            help="0 ile 1 arasında oran (ör: 0.55 = siparişlerin %55'i yeniden sipariş)",
            value=0.55,
            step=0.05,
            min_value=0.0,
            max_value=1.0,
        )

        features["user_total_orders"] = st.number_input(
            "Kullanıcının toplam sipariş sayısı (adet)",
            help="Müşterinin sistemde verdiği toplam sipariş sayısı",
            value=20.00,
            step=1.0,
            min_value=0.0,
        )

        features["user_avg_days_between_orders"] = st.number_input(
            "Siparişler arasındaki ortalama gün",
            help="Müşterinin siparişleri arasındaki ortalama gün sayısı (genelde 0–30 arası)",
            value=7.00,
            step=1.0,
            min_value=0.0,
        )

    with col_product:
        st.markdown("### Ürün / kategori özellikleri")

        features["product_reorder_rate"] = st.number_input(
            "Ürünün geçmiş yeniden sipariş oranı",
            help="0 ile 1 arasında oran (ör: 0.50 = siparişlerin %50'sinde ürün tekrar alınmış)",
            value=0.50,
            step=0.05,
            min_value=0.0,
            max_value=1.0,
        )

        features["product_avg_cart_position"] = st.number_input(
            "Ürünün sepetteki ortalama sırası",
            help="Siparişlerde ürünün sepete eklenme sırasının ortalaması",
            value=5.00,
            step=1.0,
            min_value=1.0,
        )

        features["product_order_count"] = st.number_input(
            "Ürünün toplam sipariş sayısı (adet)",
            help="Bu ürünün tüm müşterilerde kaç kez sipariş edildiği",
            value=100.00,
            step=10.0,
            min_value=0.0,
        )

        features["aisle_reorder_rate"] = st.number_input(
            "Reyon (aisle) bazında yeniden sipariş oranı",
            help="0 ile 1 arasında oran (ör: 0.30 = reyondaki ürünlerin %30'u yeniden sipariş)",
            value=0.30,
            step=0.05,
            min_value=0.0,
            max_value=1.0,
        )

    if not feature_list:
        st.warning("Feature listesi yüklenemedi. Modelin beklediği kolon listesi boş.")

    return features


def render_json_input():
    st.subheader("JSON ile Özellik Gönder")
    st.markdown(
        "Teknik ekip için, ham feature isimleri ile JSON formatında veri gönderebilirsiniz."
    )

    example = {
        "user_exploration_score": 0.40,
        "user_reorder_ratio": 0.55,
        "user_total_orders": 20.00,
        "user_avg_days_between_orders": 7.00,
        "product_reorder_rate": 0.50,
        "product_avg_cart_position": 5.00,
        "product_order_count": 100.00,
        "aisle_reorder_rate": 0.30,
    }

    st.code(json.dumps(example, indent=2), language="json")

    raw_json = st.text_area("JSON verisini buraya yapıştırın", height=220)
    features = {}

    if raw_json.strip():
        try:
            features = json.loads(raw_json)
            st.success("JSON formatı geçerli.")
        except json.JSONDecodeError:
            st.error("JSON formatı hatalı.")
            features = {}

    return features


def call_api(features):
    payload = {"features": features}

    try:
        response = requests.post(API_URL, json=payload)
    except requests.RequestException as e:
        st.error(f"API isteğinde hata: {e}")
        return None

    if response.status_code != 200:
        st.error(f"API hata durumu: {response.status_code}")
        st.error(response.text)
        return None

    return response.json()


def main():
    st.set_page_config(page_title="Instacart Yeniden Sipariş Tahmini", layout="wide")
    st.title("Instacart Yeniden Sipariş Tahmin Uygulaması")

    st.markdown(
        """
Bu arayüz, belirli bir **kullanıcı–ürün çifti** için
bir sonraki siparişte bu ürünün yeniden alınma olasılığını tahmin eder.

- Çıktı: `0` → ürün büyük ihtimalle yeniden alınmaz  
- Çıktı: `1` → ürün büyük ihtimalle yeniden alınır
"""
    )

    with st.expander("Model çıktısı ne anlama geliyor?"):
        st.markdown(
            """
- Model, LightGBM tabanlı bir sınıflandırıcıdır.  
- Tahmin edilen değer: `yeniden sipariş olasılığı` (0 ile 1 arasında).  
- Eşik değer (`threshold`): Bu olasılığın üzeri **1 (yeniden sipariş)**,
  altı **0 (yeniden sipariş yok)** olarak etiketlenir.  
- Olasılık ile eşik arasındaki fark (margin), kararın ne kadar güçlü olduğunu gösterir.
"""
        )

    feature_list = get_feature_list()

    st.sidebar.header("Girdi Modu")
    mode = st.sidebar.radio("Seçiniz:", ("Manuel Giriş", "JSON Girişi"))

    if mode == "Manuel Giriş":
        features = render_manual_input(feature_list)
    else:
        features = render_json_input()

    if st.button("Tahmin Al") and features:
        data = call_api(features)
        if data is None:
            return

        proba = data.get("probability", 0.0)
        label = data.get("label", 0)
        threshold = data.get("threshold", 0.40)

        margin = proba - threshold

        # Tüm sayısal gösterimler 2 basamaklı
        st.metric("Yeniden sipariş olasılığı", f"{proba:.2f}")

        if proba >= threshold:
            st.success(f"Olasılık eşik değerin üzerinde (eşik: {threshold:.2f}).")
        else:
            st.warning(f"Olasılık eşik değerin altında (eşik: {threshold:.2f}).")

        st.write("### Karar Analizi")
        st.write(
            f"- Tahmin edilen olasılık: **{proba:.2f}**  \n"
            f"- Modelin karar eşiği: **{threshold:.2f}**  \n"
            f"- Aradaki fark (olasılık − eşik): **{margin:+.2f}**"
        )

        if margin >= 0:
            st.write(
                "Bu fark pozitif olduğu için model, ürünün yeniden sipariş edileceğini "
                "düşünme yönünde ağırlıklı karar veriyor."
            )
        else:
            st.write(
                "Bu fark negatif olduğu için model, ürünün yeniden sipariş edilmeyeceğini "
                "düşünme yönünde ağırlıklı karar veriyor."
            )

        if label == 1:
            st.write("Sonuç: Bu ürünün yeniden sipariş edilme olasılığı **yüksektir**.")
        else:
            st.write("Sonuç: Bu ürünün yeniden sipariş edilme olasılığı **düşüktür**.")


if __name__ == "__main__":
    main()
