import sqlite3
import random
import time
from datetime import datetime
import os

# Path to the database file inside the database folder
DB_PATH = os.path.join("database", "iot_telemetry.db")

def initialize_system():
    """Ensures the database folder exists and seeds a hardware device profile."""
    # Create database directory if it doesn't exist locally
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert a sample hardware node configuration if it doesn't exist yet
    cursor.execute('''
        INSERT OR IGNORE INTO hardware_devices (device_id, chip_architecture, location_room, installation_date, operational_status)
        VALUES ('NODE-ESP32-01', 'ESP32-D0WDQ6', 'Embedded_Systems_Lab', '2026-06-12', 'ACTIVE')
    ''')
    conn.commit()
    conn.close()

def simulate_hardware_signals():
    """Simulates analog-to-digital converter (ADC) telemetry from circuit sensors."""
    # Generating normal operational variations using statistical normal distributions
    base_temp = random.normalvariate(27.0, 1.5)    # Room temperature stable around 27°C
    base_voltage = random.normalvariate(5.0, 0.05)  # Expected 5.0V DC rail voltage
    base_current = random.normalvariate(150.0, 8.0) # Hardware components pulling ~150mA
    
    # Injecting synthetic hardware faults/glitches (1% chance for testing validation rules)
    anomaly_trigger = random.random()
    if anomaly_trigger < 0.01: 
        base_voltage = 12.8  # Unsafe voltage surge / power rail spike
    elif anomaly_trigger > 0.99:
        base_temp = -99.0    # Broken or open-circuit thermocouple sensor fault
        
    return "NODE-ESP32-01", base_temp, base_voltage, base_current

def process_and_route_data():
    initialize_system()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🛰️ Ingestion pipeline active. Streaming telemetry to SQL database... (Ctrl+C to exit)")
    
    try:
        while True:
            dev_id, temp, volt, current = simulate_hardware_signals()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # --- HARDWARE VALIDATION & DATA CLEANING LAYER ---
            
            # Fault Condition 1: Temperature Sensor Open-Circuit Fault
            if temp < -40.0 or temp > 120.0:
                print(f"⚠️ [{now}] Sensor Fault Detected on {dev_id}! Routing to Alert Logs.")
                cursor.execute('''
                    INSERT INTO hardware_alerts (device_id, timestamp, metric_type, invalid_value, severity)
                    VALUES (?, ?, ?, ?, ?)
                ''', (dev_id, now, 'THERMOCOUPLE_FAULT', temp, 'CRITICAL'))
                conn.commit()
                time.sleep(1)
                continue  # Skip inserting this bad read into clean telemetry
                
            # Fault Condition 2: Electrical Power Surge Check
            if volt > 5.5:
                print(f"🛑 [{now}] CRITICAL OVERVOLTAGE: Power rail surge detected ({round(volt, 2)}V)!")
                cursor.execute('''
                    INSERT INTO hardware_alerts (device_id, timestamp, metric_type, invalid_value, severity)
                    VALUES (?, ?, ?, ?, ?)
                ''', (dev_id, now, 'VOLTAGE_SURGE', volt, 'CRITICAL'))
                # We still log the telemetry to keep a trace of the event, but we've flagged the alert table
            
            # --- ECE MATHEMATICAL COMPUTATION ---
            # Electrical Power calculation: Power (mW) = Voltage (V) * Current (mA)
            power = volt * current
            
            # --- SQL INSERTION LAYER ---
            cursor.execute('''
                INSERT INTO sensor_telemetry (device_id, timestamp, temperature_celsius, bus_voltage, current_ma, power_mw)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (dev_id, now, round(temp, 2), round(volt, 2), round(current, 2), round(power, 2)))
            
            conn.commit()
            print(f"Logged Log -> V: {round(volt,2)}V | I: {round(current,1)}mA | P: {round(power,1)}mW")
            time.sleep(1) # Read telemetry every second
            
    except KeyboardInterrupt:
        print("\nPipeline ingestion stopped cleanly.")
    finally:
        conn.close()

if __name__ == "__main__":
    process_and_route_data()
