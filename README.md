# iot-telemetry-pipeline
# Industrial IoT Telemetry Pipeline & Analytics Engine

A robust data-engineering pipeline tailored for an ECE framework. This system simulates real-time analog-to-digital converter (ADC) readings from embedded edge devices, validates the incoming telemetry stream via a Python cleaning layer, and logs sanitized metrics into a structured relational SQL database for advanced system diagnostics.

## 🛠️ Tech Stack & Core Concepts
- **Language:** Python 3.x
- **Database Engine:** SQL (SQLite)
- **Data Analysis:** Pandas
- **ECE Domain Concepts:** Signal validation, time-series data logging, open-circuit/sensor fault detection, and automated power calculation ($P = V \times I$).

## 📊 Database Schema Design
The relational architecture uses an optimized layout to separate infrastructure metadata from volatile time-series streaming metrics:
- **`hardware_devices`**: Manages micro-controller asset registry profiles (e.g., ESP32 architectures) and physical laboratory deployments.
- **`sensor_telemetry`**: Logs high-frequency, sanitized voltage, current, temperature, and calculated power draw values.
- **`hardware_alerts`**: Intercepts and isolates system failures (e.g., critical overvoltage spikes or sensor disconnections) for debugging.

## 🚀 How to Run the Project Locally

### 1. Setup Environment
Clone this repository to your local machine, open your terminal inside the folder, and install the required data libraries:
```bash
pip install -r requirements.txt
