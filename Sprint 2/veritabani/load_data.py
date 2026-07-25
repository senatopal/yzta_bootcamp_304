import os

# Load environment variables from backend/.env if it exists
env_path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "backend", ".env"
    )
)
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

import io
import sys
import glob
import time
import pandas as pd
import numpy as np

# =====================================================================
# DATABASE CONFIGURATION
# =====================================================================
# These can be overridden via environment variables or edited directly.
DB_HOST = os.getenv("VOLTI_DB_HOST", "localhost")
DB_PORT = os.getenv("VOLTI_DB_PORT", "5432")
DB_NAME = os.getenv("VOLTI_DB_NAME", "volti_db")
DB_USER = os.getenv("VOLTI_DB_USER", "postgres")
DB_PASS = os.getenv("VOLTI_DB_PASS", "password")

# =====================================================================
# PIPELINE LOADER
# =====================================================================

def get_db_connection():
    """
    Connects to the PostgreSQL database.
    Requires psycopg2-binary package.
    """
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except ImportError:
        print("[!] Error: 'psycopg2' library is not installed.")
        print("    Please run: pip install psycopg2-binary")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error connecting to database: {e}")
        print("    Please check your database server status and credentials.")
        sys.exit(1)


def clean_val(val):
    """
    Safely converts NaN, NaT, or Null values to Python None for SQL database compatibility.
    """
    if pd.isna(val):
        return None
    return val


def load_households(conn, parquet_files):
    """
    Extracts distinct households from all Parquet files and loads them.
    Uses 'ON CONFLICT DO NOTHING' to prevent duplicate keys.
    """
    print("[*] Extracting unique households from Parquet files...")
    all_hh = []
    for file in parquet_files:
        df = pd.read_parquet(file, columns=["LCLid", "stdorToU", "Acorn_grouped"])
        df_unique = df.drop_duplicates(subset=["LCLid"])
        all_hh.append(df_unique)
        
    combined_hh = pd.concat(all_hh).drop_duplicates(subset=["LCLid"])
    print(f"    - Found {len(combined_hh)} unique households.")
    
    cursor = conn.cursor()
    inserted_count = 0
    
    # Bulk insert households using ON CONFLICT DO NOTHING
    query = """
        INSERT INTO households ("LCLid", "stdorToU", acorn_grouped)
        VALUES (%s, %s, %s)
        ON CONFLICT ("LCLid") DO NOTHING;
    """
    
    data_tuples = [
        (clean_val(row["LCLid"]), clean_val(row["stdorToU"]), clean_val(row["Acorn_grouped"]))
        for _, row in combined_hh.iterrows()
        if not pd.isna(row["LCLid"])
    ]
    
    from psycopg2.extras import execute_batch
    execute_batch(cursor, query, data_tuples)
    conn.commit()
    print("[OK] Households migration complete.")


def load_weather(conn, parquet_files):
    """
    Extracts distinct weather parameters by timestamp (tstp)
    and loads them into weather_readings.
    """
    print("[*] Extracting weather records from Parquet files...")
    weather_cols = [
        "tstp", "visibility", "windBearing", "temperature", "dewPoint",
        "pressure", "apparentTemperature", "windSpeed", "precipType",
        "icon", "humidity", "summary"
    ]
    
    all_weather = []
    for file in parquet_files:
        df = pd.read_parquet(file, columns=weather_cols)
        df_unique = df.drop_duplicates(subset=["tstp"])
        all_weather.append(df_unique)
        
    combined_weather = pd.concat(all_weather).drop_duplicates(subset=["tstp"])
    
    # Handle NaNs in weather columns (convert to None for SQL null compatibility)
    combined_weather = combined_weather.dropna(subset=["tstp"])
    print(f"    - Found {len(combined_weather)} unique half-hourly weather timestamps.")
    
    cursor = conn.cursor()
    query = """
        INSERT INTO weather_readings (
            tstp, visibility, wind_bearing, temperature, dew_point, pressure,
            apparent_temperature, wind_speed, precip_type, icon, humidity, summary
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (tstp) DO NOTHING;
    """
    
    data_tuples = [
        (
            clean_val(row["tstp"]), clean_val(row["visibility"]), clean_val(row["windBearing"]), clean_val(row["temperature"]),
            clean_val(row["dewPoint"]), clean_val(row["pressure"]), clean_val(row["apparentTemperature"]),
            clean_val(row["windSpeed"]), clean_val(row["precipType"]), clean_val(row["icon"]), clean_val(row["humidity"]), clean_val(row["summary"])
        )
        for _, row in combined_weather.iterrows()
    ]
    
    from psycopg2.extras import execute_batch
    execute_batch(cursor, query, data_tuples)
    conn.commit()
    print("[OK] Weather parameters migration complete.")


def bulk_copy_consumption(conn, file_path):
    """
    Loads consumption readings using PostgreSQL COPY protocol
    which is up to 100x faster than traditional INSERT commands.
    """
    print(f"[*] Bulk loading consumption readings from {os.path.basename(file_path)}...")
    
    # Read only the required columns
    df = pd.read_parquet(file_path, columns=["tstp", "LCLid", "energy(kWh/hh)", "price_pence", "cost_pounds"])
    
    # Convert dataframe into an in-memory CSV string buffer
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, sep='\t', header=False, index=False, na_rep='\\N')
    csv_buffer.seek(0)
    
    cursor = conn.cursor()
    
    # High-speed COPY command execution
    copy_query = r"""
        COPY consumption_readings (tstp, "LCLid", energy_kwh, price_pence, cost_pounds)
        FROM STDIN WITH (FORMAT CSV, DELIMITER E'\t', NULL '\N');
    """
    
    try:
        cursor.copy_expert(copy_query, csv_buffer)
        conn.commit()
        print(f"    - Successfully loaded {len(df)} rows.")
    except Exception as e:
        conn.rollback()
        print(f"[!] Error bulk copying file: {e}")
        # Sometimes key collisions occur if re-running without truncate
        print("    If key collisions occurred, make sure tables are empty before load.")


def main():
    print("=== Volti High-Performance Database Loader ===")
    
    # Find processed Parquet files
    parquet_pattern = "dataset/block_*.parquet"
    parquet_files = sorted(glob.glob(parquet_pattern))
    
    if not parquet_files:
        print(f"[!] No parquet files found matching pattern: {parquet_pattern}")
        print("    Please run the data preparation notebook first to export parquets to dataset/.")
        sys.exit(1)
        
    print(f"[*] Found {len(parquet_files)} parquet files for migration.")
    
    # Connect
    conn = get_db_connection()
    
    # 1. Load Households Metadata
    t0 = time.time()
    load_households(conn, parquet_files)
    
    # 2. Load Weather Parameters
    load_weather(conn, parquet_files)
    
    # 3. Load Consumption readings via COPY stream
    print("[*] Migrating consumption readings (hypertables)...")
    for file in parquet_files:
        bulk_copy_consumption(conn, file)
        
    conn.close()
    print("==================================================")
    print(f"[OK] Database migration complete in {time.time() - t0:.2f}s!")


if __name__ == "__main__":
    main()
