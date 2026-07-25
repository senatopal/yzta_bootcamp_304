import pandas as pd
from datetime import timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.consumption import ConsumptionReading
from app.services.simulation import SimulationService

class CoachService:
    @classmethod
    def get_grounding_context(cls, db: Session, household_id: str) -> Dict[str, Any]:
        # 1. Find the latest reading timestamp for this household to set the end date of our 7-day window
        latest_reading = (
            db.query(ConsumptionReading)
            .filter(ConsumptionReading.LCLid == household_id)
            .order_by(ConsumptionReading.tstp.desc())
            .first()
        )

        if not latest_reading:
            return {
                "household_id": household_id,
                "weekly_summary": None,
                "cheapest_hours": [],
                "expensive_hours": [],
                "recommendations": [],
                "anomalies": [],
                "prompt_context": f"No energy consumption data is currently available in the database for household {household_id}."
            }

        end_date = latest_reading.tstp
        start_date = end_date - timedelta(days=7)

        # 2. Query all readings in the 7-day range
        readings = (
            db.query(ConsumptionReading)
            .filter(
                ConsumptionReading.LCLid == household_id,
                ConsumptionReading.tstp >= start_date,
                ConsumptionReading.tstp <= end_date
            )
            .order_by(ConsumptionReading.tstp.asc())
            .all()
        )

        if not readings:
            return {
                "household_id": household_id,
                "weekly_summary": None,
                "cheapest_hours": [],
                "expensive_hours": [],
                "recommendations": [],
                "anomalies": [],
                "prompt_context": f"No energy consumption data was found for household {household_id} between {start_date.isoformat()} and {end_date.isoformat()}."
            }

        # 3. Load readings into pandas DataFrame
        df = pd.DataFrame([
            {
                "tstp": r.tstp,
                "energy(kWh/hh)": r.energy_kwh,
                "price_pence": r.price_pence,
                "cost_pounds": r.cost_pounds
            }
            for r in readings
        ])

        # 4. Invoke SimulationService calculations
        metrics = SimulationService.calculate_tariffs(df)
        total_consumption_kwh = metrics["total_consumption_kwh"]
        total_cost_pounds = metrics["total_cost_pounds"]
        total_cost_pence = metrics["total_cost_pence"]

        # Calculate average price paid per kWh (weighted average)
        if total_consumption_kwh > 0:
            avg_price_pence = round((df['energy(kWh/hh)'] * df['price_pence']).sum() / total_consumption_kwh, 2)
        else:
            avg_price_pence = round(df['price_pence'].mean(), 2)

        carbon_impact = SimulationService.calculate_carbon_impact(total_consumption_kwh)

        # Peak hours analysis
        hours_analysis = SimulationService.analyze_critical_hours(df)
        cheapest_hours = hours_analysis["cheapest_hours"]
        expensive_hours = hours_analysis["expensive_hours"]

        # Recommendations
        rec_data = SimulationService.generate_load_shift_recommendations(df, household_id)
        recommendations = rec_data["recommendations"]
        total_savings_pounds = rec_data["total_savings_pounds"]

        # Anomalies
        anomaly_data = SimulationService.detect_anomaly(df, household_id)
        anomalies = anomaly_data["anomalies"]
        anomaly_detected = anomaly_data["anomaly_detected"]

        # 5. Format prompt context block
        prompt_context = (
            f"You are the Volti Energy Coach, an AI assistant helping household {household_id} save energy and money.\n"
            f"Grounding Data for Household: {household_id}\n"
            f"Analysis Period: {start_date.strftime('%Y-%m-%d %H:%M')} to {end_date.strftime('%Y-%m-%d %H:%M')} (Last 7 days of available readings)\n\n"
            f"1. Energy Consumption Summary:\n"
            f"- Total Consumption: {total_consumption_kwh:.2f} kWh\n"
            f"- Total Cost: £{total_cost_pounds:.2f} ({total_cost_pence:.2f} pence)\n"
            f"- Weighted Average Cost per kWh: {avg_price_pence:.2f} pence\n"
            f"- Estimated Carbon Footprint: {carbon_impact['carbon_kg']:.2f} kg CO2\n\n"
            f"2. Daily Tariff Peak & Off-Peak Analysis:\n"
            f"- Top 3 Cheapest Hours (best to run appliances):\n"
        )
        for hour in cheapest_hours:
            prompt_context += f"  * {hour['time_slot']}: avg price {hour['avg_price_pence']:.2f}p, avg consumption {hour['avg_consumption_kwh']:.3f} kWh\n"
        
        prompt_context += "- Top 3 Most Expensive Hours (avoid running high energy appliances):\n"
        for hour in expensive_hours:
            prompt_context += f"  * {hour['time_slot']}: avg price {hour['avg_price_pence']:.2f}p, avg consumption {hour['avg_consumption_kwh']:.3f} kWh\n\n"

        prompt_context += f"3. Load Shifting Recommendations (Estimated Total Savings: £{total_savings_pounds:.2f}):\n"
        if recommendations:
            for rec in recommendations:
                prompt_context += f"- {rec['device']} ({rec['icon']}): Shift from {rec['current_hour']} to {rec['recommended_hour']} to save £{rec['estimated_savings_pounds']:.2f} ({rec['saving_percent']}% cost reduction, avoids {rec['carbon_reduction_kg']:.2f} kg CO2). Recommendation: {rec['message']}\n"
        else:
            prompt_context += "- No dynamic tariff savings recommendations available.\n"

        prompt_context += "\n4. Waste & Anomaly Detection:\n"
        if anomaly_detected:
            saat = anomaly_data["saat"]
            gerceklesen = anomaly_data["gerceklesen_kwh"]
            beklenen = anomaly_data["beklenen_kwh"]
            sapma = anomaly_data["sapma_yuzde"]
            msg = anomaly_data["message"]
            prompt_context += f"- WARNING: Potential energy waste / abnormal usage detected on {saat}!\n"
            prompt_context += f"  * Actual Consumption: {gerceklesen:.3f} kWh (Expected baseline: {beklenen:.3f} kWh, deviation: +{sapma:.1f}%)\n"
            prompt_context += f"  * Alert: {msg}\n"
        else:
            prompt_context += "- No abnormal consumption or energy waste was detected. Usage pattern is normal.\n"

        return {
            "household_id": household_id,
            "weekly_summary": {
                "start_date": start_date,
                "end_date": end_date,
                "total_consumption_kwh": total_consumption_kwh,
                "total_cost_pounds": total_cost_pounds,
                "average_price_pence": avg_price_pence
            },
            "cheapest_hours": cheapest_hours,
            "expensive_hours": expensive_hours,
            "recommendations": recommendations,
            "anomalies": anomalies,
            "prompt_context": prompt_context
        }
