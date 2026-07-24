# ======================================================
# Part 8
# Prediction Pipeline for LLM
# ======================================================

"""
Volti enerji tüketimi prediction pipeline.

Bu modül:
- Eğitilmiş LightGBM modelini yükler.
- Model girdilerini doğrular.
- Elektrik tüketimi tahmini üretir.
- Maliyet hesaplar.
- Gerçek tüketim varsa anomali tespiti yapar.
- LLM entegrasyonu için JSON uyumlu çıktı döndürür.

Bu dosya model eğitmez.
"""

from __future__ import annotations

import argparse
import json

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple, Union

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_ARTIFACT_PATH = (
    BASE_DIR
    / "artifacts"
    / "energy_forecast_bundle.joblib"
)

def load_model_bundle(
     artifact_path=DEFAULT_ARTIFACT_PATH
):
    
    """
    Export edilmiş model ve metadata paketini yükler.

    Parameters
    ----------
    artifact_path:
        energy_forecast_bundle.joblib dosyasının yolu.

    Returns
    -------
    dict
        Model ve metadata içeren sözlük.
    """

    artifact_path = Path(
        artifact_path
    )

    if not artifact_path.exists():
        raise FileNotFoundError(
            "Model artifact bulunamadı: "
            f"{artifact_path.resolve()}"
        )

    bundle = joblib.load(
        artifact_path
    )

    if not isinstance(bundle, dict):
        raise ValueError(
            "Model artifact sözlük formatında değil."
        )

    required_keys = {
        "model",
        "metadata"
    }

    missing_keys = (
        required_keys - set(bundle.keys())
    )

    if missing_keys:
        raise ValueError(
            "Model bundle içinde eksik alanlar var: "
            f"{sorted(missing_keys)}"
        )

    model = bundle["model"]
    metadata = bundle["metadata"]

    required_metadata = {
        "model_type",
        "feature_columns",
        "categorical_columns",
        "category_levels",
        "target_column",
        "anomaly_threshold",
        "best_iteration",
        "interval_minutes",
        "metrics"
    }

    missing_metadata = (
        required_metadata
        - set(metadata.keys())
    )

    if missing_metadata:
        raise ValueError(
            "Model metadata içinde eksik alanlar var: "
            f"{sorted(missing_metadata)}"
        )

    return bundle

def prepare_features_for_inference(
    input_df,
    metadata
):
    """
    Gelen veriyi doğrular ve model girdisini hazırlar.
    """

    if not isinstance(
        input_df,
        pd.DataFrame
    ):
        raise TypeError(
            "input_df bir pandas DataFrame olmalıdır."
        )

    if input_df.empty:
        raise ValueError(
            "Input dataframe boş olamaz."
        )

    data = input_df.copy()

    required_context_columns = [
        "LCLid",
        "tstp"
    ]

    missing_context_columns = [
        column
        for column in required_context_columns
        if column not in data.columns
    ]

    if missing_context_columns:
        raise ValueError(
            "Eksik context sütunları: "
            f"{missing_context_columns}"
        )

    data["tstp"] = pd.to_datetime(
        data["tstp"],
        errors="raise"
    )

    household_count = (
        data["LCLid"].nunique()
    )

    if household_count != 1:
        raise ValueError(
            "Input yalnızca bir haneye ait olmalıdır. "
            f"Bulunan hane sayısı: {household_count}"
        )

    duplicate_count = data.duplicated(
        subset=[
            "LCLid",
            "tstp"
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"{duplicate_count} adet yinelenen "
            "LCLid-tstp kaydı bulundu."
        )

    data = (
        data.sort_values("tstp")
        .reset_index(drop=True)
    )

    data["hour"] = (
        data["tstp"]
        .dt.hour
        .astype("int8")
    )

    data["day_of_week"] = (
        data["tstp"]
        .dt.dayofweek
        .astype("int8")
    )

    data["month"] = (
        data["tstp"]
        .dt.month
        .astype("int8")
    )

    data["is_weekend"] = (
        data["day_of_week"] >= 5
    ).astype("int8")

    required_features = metadata[
        "feature_columns"
    ]

    missing_features = [
        column
        for column in required_features
        if column not in data.columns
    ]

    if missing_features:
        raise ValueError(
            "Modelin beklediği feature sütunları eksik: "
            f"{missing_features}"
        )

    features = data[
        required_features
    ].copy()

    categorical_columns = metadata[
        "categorical_columns"
    ]

    category_levels = metadata[
        "category_levels"
    ]

    for column in categorical_columns:

        if column not in category_levels:
            raise ValueError(
                f"{column} için kategori seviyeleri "
                "metadata içinde bulunamadı."
            )

        allowed_values = set(
            str(value)
            for value in category_levels[column]
        )

        observed_values = set(
            features[column]
            .dropna()
            .astype(str)
            .unique()
        )

        unknown_values = (
            observed_values - allowed_values
        )

        if unknown_values:
            raise ValueError(
                f"{column} sütununda modelin "
                "tanımadığı kategoriler var: "
                f"{sorted(unknown_values)}"
            )

        features[column] = pd.Categorical(
            features[column],
            categories=category_levels[column]
        )

    if list(features.columns) != list(
        required_features
    ):
        raise ValueError(
            "Feature sütun sırası metadata ile uyuşmuyor."
        )

    return data, features

def predict_consumption(
    input_df,
    artifact_path=DEFAULT_ARTIFACT_PATH
):
    """
    Input verisini hazırlar ve tüketim tahmini üretir.

    Returns
    -------
    results:
        Hane, zaman ve tahmin değerlerini içeren dataframe.

    metadata:
        Model metadata bilgileri.
    """

    bundle = load_model_bundle(
        artifact_path
    )

    model = bundle["model"]
    metadata = bundle["metadata"]

    if metadata["model_type"] != "LightGBM":
        raise ValueError(
            "Bu pipeline yalnızca LightGBM "
            "modeli için hazırlanmıştır."
        )

    data, features = (
        prepare_features_for_inference(
            input_df,
            metadata
        )
    )

    best_iteration = metadata.get(
        "best_iteration"
    )

    predict_parameters = {}

    if best_iteration is not None:
        predict_parameters[
            "num_iteration"
        ] = int(best_iteration)

    predictions = model.predict(
        features,
        **predict_parameters
    )

    # Elektrik tüketimi negatif olamaz.
    predictions = np.clip(
        predictions,
        0,
        None
    )

    results = data[
        [
            "LCLid",
            "tstp"
        ]
    ].copy()

    results["predicted_kwh"] = (
        predictions
    )

     # ==================================================
    # Cost Calculation
    # ==================================================

    results["price_pence"] = (
        data["price_pence"].to_numpy()
    )

    results["predicted_cost_pounds"] = (
        results["predicted_kwh"]
        * results["price_pence"]
        / 100
    )

    # ==================================================
    # Anomaly Detection
    # ==================================================

    target_column = metadata[
        "target_column"
    ]

    # Gelecek verisinde gerçek tüketim bulunmayabilir.
    # Gerçek tüketim varsa anomali hesaplanır.
    if target_column in data.columns:

        results["actual_kwh"] = (
            data[target_column].to_numpy()
        )

        results["residual"] = (
            results["actual_kwh"]
            - results["predicted_kwh"]
        )

        anomaly_threshold = float(
            metadata["anomaly_threshold"]
        )

        if anomaly_threshold <= 0:
            raise ValueError(
                "Anomali eşiği sıfırdan "
                "büyük olmalıdır."
            )

        results["anomaly_score"] = (
            results["residual"]
            / anomaly_threshold
        )

        results["is_anomaly"] = (
            results["residual"]
            > anomaly_threshold
        )

        severity_conditions = [
            results["anomaly_score"] >= 3,
            results["anomaly_score"] >= 2,
            results["anomaly_score"] >= 1
        ]

        severity_values = [
            "high",
            "medium",
            "low"
        ]

        results["severity"] = np.select(
            severity_conditions,
            severity_values,
            default="normal"
        )

    return results, metadata

def create_llm_payload(
    results,
    metadata,
    max_anomalies=10
):
    """
    Tahmin dataframe'ini LLM için JSON uyumlu
    Python sözlüğüne dönüştürür.
    """

    if results.empty:
        raise ValueError(
            "JSON çıktısı için results boş olamaz."
        )

    results = (
        results.sort_values("tstp")
        .reset_index(drop=True)
        .copy()
    )

    # En yüksek tüketim beklenen üç dönem
    peak_rows = results.nlargest(
        3,
        "predicted_kwh"
    )

    peak_periods = []

    for _, row in peak_rows.iterrows():

        peak_periods.append({
            "timestamp": (
                row["tstp"].isoformat()
            ),
            "predicted_kwh": round(
                float(row["predicted_kwh"]),
                4
            )
        })

    # Bütün yarım saatlik tahminler
    intervals = []

    for _, row in results.iterrows():

        intervals.append({
            "timestamp": (
                row["tstp"].isoformat()
            ),
            "predicted_kwh": round(
                float(row["predicted_kwh"]),
                4
            ),
            "price_pence": round(
                float(row["price_pence"]),
                4
            ),
            "estimated_cost_pounds": round(
                float(
                    row["predicted_cost_pounds"]
                ),
                4
            )
        })

    # Anomaliler gerçek tüketim varsa üretilir.
    anomalies = []

    if "is_anomaly" in results.columns:

        anomaly_rows = (
            results[
                results["is_anomaly"]
            ]
            .sort_values(
                "anomaly_score",
                ascending=False
            )
            .head(max_anomalies)
        )

        for _, row in anomaly_rows.iterrows():

            anomalies.append({
                "timestamp": (
                    row["tstp"].isoformat()
                ),
                "actual_kwh": round(
                    float(row["actual_kwh"]),
                    4
                ),
                "expected_kwh": round(
                    float(row["predicted_kwh"]),
                    4
                ),
                "residual_kwh": round(
                    float(row["residual"]),
                    4
                ),
                "anomaly_score": round(
                    float(row["anomaly_score"]),
                    2
                ),
                "severity": str(
                    row["severity"]
                ),
                "type": (
                    "unexpected_high_consumption"
                )
            })

    total_predicted_kwh = float(
        results["predicted_kwh"].sum()
    )

    total_predicted_cost = float(
        results[
            "predicted_cost_pounds"
        ].sum()
    )

    payload = {
        "schema_version": metadata[
            "schema_version"
        ],
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "household_id": str(
            results["LCLid"].iloc[0]
        ),
        "forecast": {
            "start": (
                results["tstp"]
                .min()
                .isoformat()
            ),
            "end": (
                results["tstp"]
                .max()
                .isoformat()
            ),
            "interval_minutes": int(
                metadata["interval_minutes"]
            ),
            "total_predicted_kwh": round(
                total_predicted_kwh,
                4
            ),
            "estimated_cost_pounds": round(
                total_predicted_cost,
                4
            ),
            "peak_periods": peak_periods,
            "intervals": intervals
        },
        "anomalies": anomalies,
        "model": {
            "type": str(
                metadata["model_type"]
            ),
            "mae": float(
                metadata["metrics"]["mae"]
            ),
            "rmse": float(
                metadata["metrics"]["rmse"]
            ),
            "r2": float(
                metadata["metrics"]["r2"]
            )
        }
    }

    return payload

def create_llm_payload(
    results,
    metadata,
    max_anomalies=10
):
    """
    Tahmin dataframe'ini LLM için JSON uyumlu
    Python sözlüğüne dönüştürür.
    """

    if results.empty:
        raise ValueError(
            "JSON çıktısı için results boş olamaz."
        )

    results = (
        results.sort_values("tstp")
        .reset_index(drop=True)
        .copy()
    )

    # En yüksek tüketim beklenen üç dönem
    peak_rows = results.nlargest(
        3,
        "predicted_kwh"
    )

    peak_periods = []

    for _, row in peak_rows.iterrows():

        peak_periods.append({
            "timestamp": (
                row["tstp"].isoformat()
            ),
            "predicted_kwh": round(
                float(row["predicted_kwh"]),
                4
            )
        })

    # Bütün yarım saatlik tahminler
    intervals = []

    for _, row in results.iterrows():

        intervals.append({
            "timestamp": (
                row["tstp"].isoformat()
            ),
            "predicted_kwh": round(
                float(row["predicted_kwh"]),
                4
            ),
            "price_pence": round(
                float(row["price_pence"]),
                4
            ),
            "estimated_cost_pounds": round(
                float(
                    row["predicted_cost_pounds"]
                ),
                4
            )
        })

    # Anomaliler gerçek tüketim varsa üretilir.
    anomalies = []

    if "is_anomaly" in results.columns:

        anomaly_rows = (
            results[
                results["is_anomaly"]
            ]
            .sort_values(
                "anomaly_score",
                ascending=False
            )
            .head(max_anomalies)
        )

        for _, row in anomaly_rows.iterrows():

            anomalies.append({
                "timestamp": (
                    row["tstp"].isoformat()
                ),
                "actual_kwh": round(
                    float(row["actual_kwh"]),
                    4
                ),
                "expected_kwh": round(
                    float(row["predicted_kwh"]),
                    4
                ),
                "residual_kwh": round(
                    float(row["residual"]),
                    4
                ),
                "anomaly_score": round(
                    float(row["anomaly_score"]),
                    2
                ),
                "severity": str(
                    row["severity"]
                ),
                "type": (
                    "unexpected_high_consumption"
                )
            })

    total_predicted_kwh = float(
        results["predicted_kwh"].sum()
    )

    total_predicted_cost = float(
        results[
            "predicted_cost_pounds"
        ].sum()
    )

    payload = {
        "schema_version": metadata[
            "schema_version"
        ],
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "household_id": str(
            results["LCLid"].iloc[0]
        ),
        "forecast": {
            "start": (
                results["tstp"]
                .min()
                .isoformat()
            ),
            "end": (
                results["tstp"]
                .max()
                .isoformat()
            ),
            "interval_minutes": int(
                metadata["interval_minutes"]
            ),
            "total_predicted_kwh": round(
                total_predicted_kwh,
                4
            ),
            "estimated_cost_pounds": round(
                total_predicted_cost,
                4
            ),
            "peak_periods": peak_periods,
            "intervals": intervals
        },
        "anomalies": anomalies,
        "model": {
            "type": str(
                metadata["model_type"]
            ),
            "mae": float(
                metadata["metrics"]["mae"]
            ),
            "rmse": float(
                metadata["metrics"]["rmse"]
            ),
            "r2": float(
                metadata["metrics"]["r2"]
            )
        }
    }

    return payload

def predict_for_llm(
    input_df,
    artifact_path=DEFAULT_ARTIFACT_PATH
):
    """
    Model tahmini üretir ve sonucu LLM JSON
    sözlüğü olarak döndürür.
    """

    results, metadata = predict_consumption(
        input_df=input_df,
        artifact_path=artifact_path
    )

    payload = create_llm_payload(
        results=results,
        metadata=metadata
    )

    return payload

def read_input_file(
    input_path
):
    """
    CSV veya Parquet dosyasını dataframe olarak okur.
    """

    input_path = Path(
        input_path
    )

    if not input_path.exists():
        raise FileNotFoundError(
            "Input dosyası bulunamadı: "
            f"{input_path.resolve()}"
        )

    extension = (
        input_path.suffix.lower()
    )

    if extension == ".parquet":

        return pd.read_parquet(
            input_path
        )

    if extension == ".csv":

        return pd.read_csv(
            input_path
        )

    raise ValueError(
        "Desteklenmeyen input formatı. "
        "Yalnızca .parquet ve .csv kullanılabilir."
    )

def save_json_payload(
    payload,
    output_path
):
    """
    LLM payload sonucunu JSON dosyasına kaydeder.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    json_output = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2
    )

    output_path.write_text(
        json_output,
        encoding="utf-8"
    )

    return output_path

def main():
    """
    Pipeline'ın terminalden çalıştırılmasını sağlar.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Volti enerji tüketimi tahmin pipeline."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        help=(
            "Feature-ready .parquet veya "
            ".csv input dosyasının yolu."
        )
    )

    parser.add_argument(
        "--output",
        required=True,
        help=(
            "Üretilecek JSON dosyasının yolu."
        )
    )

    parser.add_argument(
        "--artifact",
        default=str(
            DEFAULT_ARTIFACT_PATH
        ),
        help=(
            "Model artifact dosyasının yolu."
        )
    )

    args = parser.parse_args()

    input_df = read_input_file(
        args.input
    )

    payload = predict_for_llm(
        input_df=input_df,
        artifact_path=args.artifact
    )

    output_path = save_json_payload(
        payload=payload,
        output_path=args.output
    )

    print(
        "Prediction pipeline başarıyla tamamlandı."
    )

    print(
        f"Household: "
        f"{payload['household_id']}"
    )

    print(
        "Total predicted kWh: "
        f"{payload['forecast']['total_predicted_kwh']}"
    )

    print(
        "Estimated cost: "
        f"{payload['forecast']['estimated_cost_pounds']} pounds"
    )

    print(
        "Detected anomalies: "
        f"{len(payload['anomalies'])}"
    )

    print(
        f"JSON output: "
        f"{output_path.resolve()}"
    )

if __name__ == "__main__":
    main()