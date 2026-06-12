import sqlite3
import pandas as pd
import os

# Path to the database file
DB_PATH = os.path.join("database", "iot_telemetry.db")

def run_hardware_diagnostics():
    """Queries the SQL database and generates aggregate system health reports."""
    
    # Check if the database exists before trying to connect
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database file not found at {DB_PATH}.")
        print("Please run pipeline.py first to generate the telemetry database!")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # Advanced SQL Query: Computes operational metrics per edge device
    telemetry_query = """
    SELECT 
        device_id,
        COUNT(*) as total_samples,
        ROUND(AVG(temperature_celsius), 2) as avg_temp_c,
        ROUND(MIN(bus_voltage), 2) as min_voltage_v,
        ROUND(MAX(bus_voltage), 2) as max_voltage_v,
        ROUND(AVG(power_mw), 2) as avg_power_draw_mw
    FROM sensor_telemetry
    GROUP BY device_id;
    """
    
    print("\n📊 --- EDGE DEVICE HEALTH SUMMARY ---")
    try:
        report = pd.read_sql_query(telemetry_query, conn)
        if report.empty:
            print("No telemetry data found yet. Let pipeline.py run a bit longer!")
        else:
            print(report.to_string(index=False))
    except Exception as e:
        print(f"Database query error: {e}")
        
    # Query to fetch outstanding critical alerts
    alert_query = """
    SELECT timestamp, device_id, metric_type, invalid_value, severity 
    FROM hardware_alerts 
    ORDER BY timestamp DESC 
    LIMIT 5;
    """
    
    print("\n🚨 --- RECENT HARDWARE FAULTS & ALERTS ---")
    try:
        alerts = pd.read_sql_query(alert_query, conn)
        if alerts.empty:
            print("✅ System Stable: No hardware faults or voltage surges logged.")
        else:
            print(alerts.to_string(index=False))
    except Exception as e:
        print(f"Database query error: {e}")
        
    conn.close()

if __name__ == "__main__":
    run_hardware_diagnostics()
