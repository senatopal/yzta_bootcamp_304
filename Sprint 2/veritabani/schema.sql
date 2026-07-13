-- Volti Project - PostgreSQL & TimescaleDB Database Schema
-- Optimized for Smart Meter Time Series Data

-- Enable TimescaleDB extension if available (optional)
-- CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- 1. Households Dimension Table (Demographics and Tariffs)
CREATE TABLE IF NOT EXISTS households (
    LCLid VARCHAR(15) PRIMARY KEY,
    stdorToU VARCHAR(10) NOT NULL,
    acorn_grouped VARCHAR(30) NOT NULL
);

-- 2. Weather Parameters Table
CREATE TABLE IF NOT EXISTS weather_readings (
    tstp TIMESTAMP WITHOUT TIME ZONE PRIMARY KEY,
    visibility REAL,
    wind_bearing REAL,
    temperature REAL,
    dew_point REAL,
    pressure REAL,
    apparent_temperature REAL,
    wind_speed REAL,
    precip_type VARCHAR(25),
    icon VARCHAR(35),
    humidity REAL,
    summary VARCHAR(65)
);

-- 3. Consumption Readings Table (Ana Zaman Serisi Tablosu)
CREATE TABLE IF NOT EXISTS consumption_readings (
    tstp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    LCLid VARCHAR(15) NOT NULL REFERENCES households(LCLid),
    energy_kwh REAL,
    price_pence REAL,
    cost_pounds REAL,
    PRIMARY KEY (LCLid, tstp)
);

-- TimescaleDB Hypertable Definition
-- Partitioning the consumption table by the 'tstp' time dimension
-- (If TimescaleDB extension is active in your database, execute this line)
-- SELECT create_hypertable('consumption_readings', 'tstp', if_not_exists => TRUE);

-- Performance Indexes
-- Index for quick global datetime scans (e.g. general grid load at a specific hour)
CREATE INDEX IF NOT EXISTS idx_consumption_tstp ON consumption_readings (tstp DESC);

-- Composite index for fast household-level time series historical lookup
CREATE INDEX IF NOT EXISTS idx_consumption_lclid_tstp ON consumption_readings (LCLid, tstp DESC);
