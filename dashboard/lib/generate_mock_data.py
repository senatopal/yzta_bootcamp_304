import pandas as pd
import numpy as np
import json
import os

# Mock veri dosyalarini data/ klasorune kaydet
os.makedirs("data", exist_ok=True)

np.random.seed(42)

# 1) TUKETIM VERISI (mock_consumption.csv)
# Bir gunun 48 yarim saatlik dilimi
# Gercek tuketim + model tahmini
timestamps = pd.date_range("2024-01-15 00:00", periods=48, freq="30min")

# Gercekci tuketim profili: gece dusuk, sabah yukseliyor, aksam pik
hours = timestamps.hour + timestamps.minute / 60
base_consumption = np.where(
    hours < 6, np.random.uniform(0.15, 0.35, 48),          # Gece: dusuk
    np.where(hours < 9, np.random.uniform(0.5, 1.0, 48),   # Sabah: orta
    np.where(hours < 16, np.random.uniform(0.3, 0.6, 48),  # Gunduz: dusuk-orta
    np.where(hours < 21, np.random.uniform(1.0, 1.8, 48),  # Aksam pik: yuksek
    np.random.uniform(0.2, 0.5, 48)                         # Gece: dusuk
))))

# Tahmin = gercek + kucuk bir hata
predicted = base_consumption + np.random.normal(0, 0.08, 48)
predicted = np.clip(predicted, 0.05, 2.5)

consumption_df = pd.DataFrame({
    "timestamp": timestamps.strftime("%Y-%m-%d %H:%M"),
    "consumption_kwh": np.round(base_consumption, 3),
    "predicted_kwh": np.round(predicted, 3)
})

consumption_df.to_csv("data/mock_consumption.csv", index=False)
print("mock_consumption.csv olusturuldu")

# 2) TARIFE VERISI (mock_tariff.csv)
# Londra dinamik tarife (Time-of-Use)
# Pence/kWh cinsinden
tariff_prices = []
for i in range(48):
    h = i / 2  # saat
    if 0 <= h < 7:        # Gece (ucuz)
        price = np.random.uniform(5, 8)
    elif 7 <= h < 16:     # Gunduz (orta)
        price = np.random.uniform(15, 20)
    elif 16 <= h < 21:    # Aksam pik (pahali)
        price = np.random.uniform(25, 35)
    else:                  # Gec gece (ucuz)
        price = np.random.uniform(7, 12)
    tariff_prices.append(round(price, 1))

tariff_df = pd.DataFrame({
    "timestamp": timestamps.strftime("%Y-%m-%d %H:%M"),
    "price_pence_kwh": tariff_prices
})

tariff_df.to_csv("data/mock_tariff.csv", index=False)
print("mock_tariff.csv olusturuldu")


# 3) ONERILER (mock_recommendations.json)
# Yuk kaydirma onerileri
recommendations = [
    {
        "cihaz": "Camasir Makinesi",
        "ikon": "👕",
        "mevcut_saat": "18:00",
        "onerilen_saat": "02:00",
        "tasarruf_sterlin": 0.85,
        "tasarruf_co2_kg": 0.18
    },
    {
        "cihaz": "Bulasik Makinesi",
        "ikon": "🍽️",
        "mevcut_saat": "19:30",
        "onerilen_saat": "03:00",
        "tasarruf_sterlin": 0.62,
        "tasarruf_co2_kg": 0.13
    },
    {
        "cihaz": "Elektrikli Arac Sarj",
        "ikon": "🔌",
        "mevcut_saat": "17:00",
        "onerilen_saat": "01:00",
        "tasarruf_sterlin": 1.45,
        "tasarruf_co2_kg": 0.31
    },
    {
        "cihaz": "Kurutma Makinesi",
        "ikon": "🌀",
        "mevcut_saat": "20:00",
        "onerilen_saat": "04:00",
        "tasarruf_sterlin": 0.53,
        "tasarruf_co2_kg": 0.11
    }
]

with open("data/mock_recommendations.json", "w", encoding="utf-8") as f:
    json.dump(recommendations, f, ensure_ascii=False, indent=2)
print("mock_recommendations.json olusturuldu")

# 4) ANOMALI (mock_anomaly.json)

anomaly = {
    "anomali_var": True,
    "saat": "18:30",
    "beklenen_kwh": 1.2,
    "gerceklesen_kwh": 2.1,
    "sapma_yuzde": 75,
    "mesaj": "18:30'da tuketim normalin %75 uzerinde!"
}

with open("data/mock_anomaly.json", "w", encoding="utf-8") as f:
    json.dump(anomaly, f, ensure_ascii=False, indent=2)
print("mock_anomaly.json olusturuldu")

# ============================================================
# 5) OZET (mock_summary.json)
# ============================================================
total_consumption = round(consumption_df["consumption_kwh"].sum(), 2)
total_cost_pence = sum(
    consumption_df["consumption_kwh"].iloc[i] * tariff_df["price_pence_kwh"].iloc[i]
    for i in range(48)
)
total_cost_sterlin = round(total_cost_pence / 100, 2)
total_saving = round(0.85 + 0.62 + 1.45 + 0.53, 2)  # Tum onerilerin toplami
total_co2 = round(0.18 + 0.13 + 0.31 + 0.11, 2)

summary = {
    "gunluk_tuketim_kwh": total_consumption,
    "tahmini_maliyet_sterlin": total_cost_sterlin,
    "tasarruf_potansiyeli_sterlin": total_saving,
    "co2_azaltma_kg": total_co2,
    "en_ucuz_saatler": "00:00 - 07:00",
    "en_pahali_saatler": "16:00 - 21:00"
}

with open("data/mock_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print("mock_summary.json olusturuldu")

print("\n Tum mock veriler data/ klasorune kaydedildi!")
print(f"  Gunluk tuketim: {total_consumption} kWh")
print(f"  Tahmini maliyet: £{total_cost_sterlin}")
print(f"  Tasarruf potansiyeli: £{total_saving}")
print(f"  CO2 azaltma: {total_co2} kg")