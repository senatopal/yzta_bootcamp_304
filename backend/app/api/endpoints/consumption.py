from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from app.core.database import get_db
from app.models.consumption import ConsumptionReading
from app.schemas.consumption import ConsumptionHistoryResponse, ConsumptionHistoryPoint

router = APIRouter()

@router.get(
    "/consumption/history",
    response_model=ConsumptionHistoryResponse,
    tags=["Consumption"]
)
def get_consumption_history(
    household_id: str = Query(..., description="LCLid of the household"),
    period: str = Query("daily", description="Aggregation period: half-hourly, daily, weekly, monthly"),
    start_date: Optional[datetime] = Query(None, description="Start date filter (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="End date filter (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Retrieves the historical electricity consumption for a specific household,
    with aggregation support for daily, weekly, and monthly intervals.
    """
    if period not in ["half-hourly", "daily", "weekly", "monthly"]:
        raise HTTPException(status_code=400, detail="Invalid period. Must be one of: half-hourly, daily, weekly, monthly")

    # Base query filtering by household
    query = db.query(ConsumptionReading).filter(ConsumptionReading.LCLid == household_id)
    if start_date:
        query = query.filter(ConsumptionReading.tstp >= start_date)
    if end_date:
        query = query.filter(ConsumptionReading.tstp <= end_date)

    data_points = []

    if period == "half-hourly":
        # Raw half-hourly records, no aggregation needed
        records = query.order_by(ConsumptionReading.tstp.asc()).all()
        for r in records:
            data_points.append(
                ConsumptionHistoryPoint(
                    timestamp=r.tstp.strftime("%Y-%m-%d %H:%M:%S"),
                    consumption_kwh=round(r.energy_kwh, 4) if r.energy_kwh is not None else 0.0,
                    cost_pounds=round(r.cost_pounds, 4) if r.cost_pounds is not None else 0.0,
                    avg_price_pence=round(r.price_pence, 4) if r.price_pence is not None else 0.0
                )
            )
    else:
        # Grouped periods: daily, weekly, monthly
        # We detect database dialect (e.g. SQLite for unit tests, PostgreSQL for production)
        is_sqlite = db.bind.dialect.name == "sqlite"

        if is_sqlite:
            if period == "daily":
                time_bucket = func.strftime('%Y-%m-%d', ConsumptionReading.tstp)
            elif period == "weekly":
                time_bucket = func.strftime('%Y-%W', ConsumptionReading.tstp)
            else: # monthly
                time_bucket = func.strftime('%Y-%m', ConsumptionReading.tstp)
        else: # postgresql
            if period == "daily":
                time_bucket = func.date_trunc('day', ConsumptionReading.tstp)
            elif period == "weekly":
                time_bucket = func.date_trunc('week', ConsumptionReading.tstp)
            else: # monthly
                time_bucket = func.date_trunc('month', ConsumptionReading.tstp)

        # Aggregate query
        agg_query = db.query(
            time_bucket.label("bucket"),
            func.sum(ConsumptionReading.energy_kwh).label("total_energy_kwh"),
            func.sum(ConsumptionReading.cost_pounds).label("total_cost_pounds"),
            func.avg(ConsumptionReading.price_pence).label("avg_price_pence")
        ).filter(ConsumptionReading.LCLid == household_id)

        if start_date:
            agg_query = agg_query.filter(ConsumptionReading.tstp >= start_date)
        if end_date:
            agg_query = agg_query.filter(ConsumptionReading.tstp <= end_date)

        results = agg_query.group_by(time_bucket).order_by(time_bucket.asc()).all()

        for row in results:
            if row.bucket is None:
                continue

            # Convert result to string timestamp format
            if isinstance(row.bucket, str):
                ts_str = row.bucket
            else: # datetime from PostgreSQL
                if period == "daily":
                    ts_str = row.bucket.strftime("%Y-%m-%d")
                elif period == "weekly":
                    ts_str = row.bucket.strftime("%Y-W%W")
                else: # monthly
                    ts_str = row.bucket.strftime("%Y-%m")

            data_points.append(
                ConsumptionHistoryPoint(
                    timestamp=ts_str,
                    consumption_kwh=round(row.total_energy_kwh, 4) if row.total_energy_kwh is not None else 0.0,
                    cost_pounds=round(row.total_cost_pounds, 4) if row.total_cost_pounds is not None else 0.0,
                    avg_price_pence=round(row.avg_price_pence, 4) if row.avg_price_pence is not None else 0.0
                )
            )

    return ConsumptionHistoryResponse(
        household_id=household_id,
        period=period,
        data=data_points
    )
