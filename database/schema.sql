-- 1. Device Registry Table
CREATE TABLE hardware_devices (
    device_id VARCHAR(50) PRIMARY KEY,
    chip_architecture VARCHAR(50), 
    location_room VARCHAR(50),     
    installation_date DATE,
    operational_status VARCHAR(20) DEFAULT 'ACTIVE'
);

-- 2. Clean Telemetry Table (Time-Series)
CREATE TABLE sensor_telemetry (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature_celsius REAL,
    bus_voltage REAL,              
    current_ma REAL,               
    power_mw REAL,                 
    FOREIGN KEY (device_id) REFERENCES hardware_devices(device_id)
);

-- 3. Incident/Anomaly Log Table
CREATE TABLE hardware_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metric_type VARCHAR(30),       
    invalid_value REAL,
    severity VARCHAR(10),          
    FOREIGN KEY (device_id) REFERENCES hardware_devices(device_id)
);
