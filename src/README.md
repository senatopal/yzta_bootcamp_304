# Volti ML Prediction Pipeline

Volti, akıllı sayaç verilerinden elektrik tüketimi tahmini, maliyet hesabı ve beklenmedik yüksek tüketim tespiti üreten bir makine öğrenmesi pipeline'ıdır.

Pipeline çıktısı JSON formatındadır ve arayüz veya LLM katmanı tarafından doğrudan kullanılabilir.

## Özellikler

- Yarım saatlik elektrik tüketimi tahmini
- Dinamik tarifeye göre tahmini maliyet hesabı
- Beklenmedik yüksek tüketim tespiti
- Anomali önem seviyesi üretimi
- LLM entegrasyonu için JSON çıktı
- Jupyter Notebook gerektirmeden çalıştırma

## Model

Final model olarak LightGBM kullanılmıştır.

Model, Smart Meters in London veri setindeki 16.036.287 yarım saatlik sayaç kaydıyla eğitilmiştir.

Model performansı:

| Metrik | Değer |
|---|---:|
| MAE | 0.1116 |
| RMSE | 0.2151 |
| R² | 0.7544 |
| Anomali eşiği | 0.7644 kWh |

## Proje Yapısı

```text
volti-ml/src
├── prediction_pipeline.py
├── requirements.txt
├── README.md
├── artifacts/
│   ├── energy_forecast_bundle.joblib
│   └── energy_forecast_metadata.json
├── examples/
│   ├── example_input.parquet
│   └── example_output.json
└── notebooks/
    └── model_training_and_test.ipynb
```

Eğitim veri blokları GitHub deposuna dahil edilmez.

## Kurulum

Önerilen Python sürümü:

```text
Python 3.13
```

Projeyi indirdikten sonra sanal ortam oluşturun:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Terminalden Kullanım

Örnek input dosyasını kullanarak pipeline'ı çalıştırın:

```powershell
python prediction_pipeline.py --input examples/example_input.parquet --output examples/example_output.json
```

Başarılı çalışmada terminalde aşağıdakine benzer bir sonuç görülür:

```text
Prediction pipeline başarıyla tamamlandı.
Household: MAC000002
Total predicted kWh: 8.7539
Estimated cost: 1.2455 pounds
Detected anomalies: 0
JSON output: examples/example_output.json
```

## Python İçinden Kullanım

Pipeline başka bir backend veya Python modülü içerisinden çağrılabilir:

```python
import pandas as pd

from prediction_pipeline import predict_for_llm

input_df = pd.read_parquet(
    "examples/example_input.parquet"
)

payload = predict_for_llm(
    input_df
)

print(payload)
```

## Input Formatı

Pipeline aynı anda yalnızca bir haneye ait kayıtları kabul eder.

Zorunlu context sütunları:

```text
LCLid
tstp
```

Modelin kullandığı feature sütunları:

```text
stdorToU
Acorn_grouped
price_pence
visibility
windBearing
temperature
dewPoint
pressure
apparentTemperature
windSpeed
precipType
icon
humidity
summary
lag_1
lag_2
lag_48
lag_336
hour
day_of_week
month
is_weekend
```

Pipeline, `hour`, `day_of_week`, `month` ve `is_weekend` sütunlarını `tstp` üzerinden yeniden hesaplar.

Anomali tespiti için aşağıdaki gerçek tüketim sütunu input içinde bulunmalıdır:

```text
energy(kWh/hh)
```

Bu sütun bulunmazsa tüketim tahmini ve maliyet hesabı yapılır ancak anomali tespiti yapılmaz.

## JSON Çıktısı

Pipeline aşağıdaki yapıda bir sözlük veya JSON dosyası üretir:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-07-24T12:00:00+00:00",
  "household_id": "MAC000002",
  "forecast": {
    "start": "2012-10-12T00:30:00",
    "end": "2012-10-13T00:00:00",
    "interval_minutes": 30,
    "total_predicted_kwh": 8.7539,
    "estimated_cost_pounds": 1.2455,
    "peak_periods": [],
    "intervals": []
  },
  "anomalies": [],
  "model": {
    "type": "LightGBM",
    "mae": 0.1116,
    "rmse": 0.2151,
    "r2": 0.7544
  }
}
```

## LLM Entegrasyonu

LLM katmanı doğrudan model artifact'ını kullanmak zorunda değildir.

Önerilen akış:

```text
Kullanıcı isteği
→ Backend input verisini hazırlar
→ predict_for_llm(input_df)
→ Tahmin JSON'u
→ LLM açıklaması
→ Arayüz
```

LLM'nin görevi hesaplama yapmak değil, pipeline tarafından üretilen sayısal sonuçları kullanıcıya anlaşılır şekilde açıklamaktır.

Örnek LLM açıklaması:

> İncelenen dönemde tahmini tüketiminiz 8,75 kWh ve tahmini maliyetiniz £1,25'tir. Bu dönemde beklenmedik yüksek tüketim tespit edilmemiştir.

## Artifact Dosyaları

`energy_forecast_bundle.joblib` aşağıdakileri içerir:

- Eğitilmiş LightGBM modeli
- Model metadata bilgileri
- Feature sırası
- Kategorik değişken bilgileri
- Anomali eşiği
- Model metrikleri

`energy_forecast_metadata.json`, aynı bilgilerin okunabilir JSON sürümüdür.

## Sınırlamalar

- Pipeline feature-ready input bekler.
- Lag sütunlarının geçmiş tüketim verisinden önceden hazırlanmış olması gerekir.
- Model Londra 2011-2014 akıllı sayaç verileriyle eğitilmiştir.
- Maliyet `price_pence` üzerinden pound cinsinden hesaplanır.
- Anomali sonucu kesin arıza teşhisi değildir; beklenmedik tüketim uyarısıdır.
- Model cihaz seviyesinde tüketim ayrıştırması yapmaz.
