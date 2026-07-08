import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json

# ============================================================
# SAYFA AYARLARI
# ============================================================
st.set_page_config(
    page_title="Volti - Enerji Tasarruf Kocun",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Volti — Enerji Tasarruf Kocun")
st.caption("Akilli sayac verinle tasarruf firsatlarini kesfet")

# ============================================================
# VERILERI OKU
# ============================================================
consumption_df = pd.read_csv("data/mock_consumption.csv")
tariff_df = pd.read_csv("data/mock_tariff.csv")

with open("data/mock_recommendations.json", "r", encoding="utf-8") as f:
    recommendations = json.load(f)

with open("data/mock_anomaly.json", "r", encoding="utf-8") as f:
    anomaly = json.load(f)

with open("data/mock_summary.json", "r", encoding="utf-8") as f:
    summary = json.load(f)

# Saat etiketi icin kisa format
consumption_df["saat"] = pd.to_datetime(consumption_df["timestamp"]).dt.strftime("%H:%M")
tariff_df["saat"] = pd.to_datetime(tariff_df["timestamp"]).dt.strftime("%H:%M")

# ============================================================
# TASARRUF OZETI METRIKLERI (Task 8)
# ============================================================
st.markdown("### 📊 Gunluk Ozet")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gunluk Tuketim", f"{summary['gunluk_tuketim_kwh']} kWh")
col2.metric("Tahmini Maliyet", f"£{summary['tahmini_maliyet_sterlin']}")
col3.metric("Tasarruf Potansiyeli", f"£{summary['tasarruf_potansiyeli_sterlin']}", delta="kazanabilirsin")
col4.metric("CO₂ Azaltma", f"{summary['co2_azaltma_kg']} kg", delta="azaltabilirsin")

st.divider()


# ANOMALI UYARI BANDI (Task 7)

if anomaly["anomali_var"]:
    st.error(f"⚠️ Anomali: {anomaly['mesaj']} (Beklenen: {anomaly['beklenen_kwh']} kWh → Gerceklesen: {anomaly['gerceklesen_kwh']} kWh)")
else:
    st.success("✅ Bugun anormal tuketim yok.")

st.divider()

# TUKETIM GRAFIGI (Task 4)
#
st.markdown("### 📈 Tuketim & Tahmin")

fig_consumption = go.Figure()

fig_consumption.add_trace(go.Scatter(
    x=consumption_df["saat"],
    y=consumption_df["consumption_kwh"],
    mode="lines+markers",
    name="Gercek Tuketim",
    line=dict(color="#3498db", width=2),
    marker=dict(size=4)
))

fig_consumption.add_trace(go.Scatter(
    x=consumption_df["saat"],
    y=consumption_df["predicted_kwh"],
    mode="lines",
    name="Model Tahmini",
    line=dict(color="#e67e22", width=2, dash="dash")
))

# Anomali bolgesini isaretle
if anomaly["anomali_var"]:
    anomali_saat = anomaly["saat"]
    fig_consumption.add_vrect(
        x0=anomali_saat, x1=anomali_saat,
        fillcolor="red", opacity=0.15,
        annotation_text="⚠️ Anomali",
        annotation_position="top left",
        line_width=2, line_color="red"
    )

fig_consumption.update_layout(
    xaxis_title="Saat",
    yaxis_title="Tuketim (kWh)",
    hovermode="x unified",
    template="plotly_dark",
    height=400,
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(fig_consumption, use_container_width=True)

st.divider()

# ============================================================
# TARIFE HARITASI (Task 5)
# ============================================================
st.markdown("### 💰 Saatlik Elektrik Fiyati")
st.caption("🟢 Ucuz saatlerde cihazlari calistir, 🔴 pahali saatlerden kacin")

# Renk: ucuz=yesil, orta=sari, pahali=kirmizi
colors = []
for price in tariff_df["price_pence_kwh"]:
    if price < 10:
        colors.append("#2ecc71")     # yesil - ucuz
    elif price < 22:
        colors.append("#f39c12")     # sari - orta
    else:
        colors.append("#e74c3c")     # kirmizi - pahali

fig_tariff = go.Figure()

fig_tariff.add_trace(go.Bar(
    x=tariff_df["saat"],
    y=tariff_df["price_pence_kwh"],
    marker_color=colors,
    hovertemplate="Saat: %{x}<br>Fiyat: %{y} p/kWh<extra></extra>"
))

fig_tariff.update_layout(
    xaxis_title="Saat",
    yaxis_title="Fiyat (pence/kWh)",
    template="plotly_dark",
    height=350,
    margin=dict(l=20, r=20, t=10, b=20)
)

st.plotly_chart(fig_tariff, use_container_width=True)

st.divider()

# ONERI KARTLARI (Task 6)
st.markdown("### 💡 Tasarruf Onerileri")
st.caption("Cihazlari ucuz saatlere kaydirarak tasarruf et")

cols = st.columns(len(recommendations))

for i, rec in enumerate(recommendations):
    with cols[i]:
        st.markdown(f"#### {rec['ikon']} {rec['cihaz']}")
        st.markdown(f"🕐 {rec['mevcut_saat']} → {rec['onerilen_saat']}")
        st.metric("Tasarruf", f"£{rec['tasarruf_sterlin']}")
        st.caption(f"🌱 {rec['tasarruf_co2_kg']} kg CO₂")

st.divider()

# LLM KOC MESAJI - PLACEHOLDER (Task 9)
st.markdown("### 🤖 Volti Koc")

with st.chat_message("assistant"):
    st.write(
        f"Merhaba! Bugunun tahmini tuketimin **{summary['gunluk_tuketim_kwh']} kWh**, "
        f"bu da yaklasik **£{summary['tahmini_maliyet_sterlin']}** demek. "
        f"\n\n"
        f"Elektrik **{summary['en_pahali_saatler']}** arasinda en pahali. "
        f"Camasir ve bulasik makinesini **{summary['en_ucuz_saatler']}** arasina kaydirirsan "
        f"toplamda **£{summary['tasarruf_potansiyeli_sterlin']}** tasarruf edebilirsin — "
        f"hem cebine hem gezegenine iyi gelir! 🌍"
    )

st.caption("Sprint 3'te bu mesaj gercek LLM (AI) tarafindan uretilecektir.")

#
# FOOTER
st.divider()
st.caption("Volti v0.1 — Mock Veri ile Prototip | Voltra Takimi")