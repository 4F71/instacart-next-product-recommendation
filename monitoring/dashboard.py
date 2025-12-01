# monitoring/dashboard.py

"""
Streamlit monitoring ekranı.
- Son tahminler
- Toplam tahmin sayısı
- Pozitif / negatif oranı
"""

from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "predictions.db"


def load_data(limit: int = 5000) -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM predictions ORDER BY created_at DESC LIMIT ?",
            conn,
            params=(limit,),
        )
    finally:
        conn.close()
    return df


def main() -> None:
    st.title("Instacart Reorder – Monitoring")

    df = load_data()

    if df.empty:
        st.info("Henüz kayıtlı tahmin yok.")
        return

    st.metric("Toplam tahmin sayısı", len(df))

    positive_rate = df["is_reorder"].mean()
    st.metric("Pozitif tahmin oranı", f"{positive_rate:.2%}")

    st.subheader("Son Tahminler")
    st.dataframe(df[["created_at", "user_id", "product_id", "probability", "is_reorder"]])

    st.subheader("Tahmin Olasılığı Dağılımı")
    st.bar_chart(df["probability"])


if __name__ == "__main__":
    main()
