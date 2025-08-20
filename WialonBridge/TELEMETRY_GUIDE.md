# Xirgo/Sensata XG3780 Telemetry Integration Guide

## Overview

This system provides comprehensive telemetry mapping for Xirgo/Sensata XG3780 GPS tracking devices through Wialon retranslator webhooks. The system automatically parses, maps, and stores detailed sensor data with proper calibration and categorization.

## Supported Data Formats

### SOAP XML (Recommended)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                  xmlns:web="http://webservice.retranslator.wialon">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>your_webhook_token</wsse:Username>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        <web:submitData>
            <unitId>XG3780_DEVICE_001</unitId>
            <latitude>40.7589</latitude>
            <longitude>-73.9851</longitude>
            <altitude>15.2</altitude>
            <speed>45.6</speed>
            <heading>180</heading>
            <timestamp>2025-08-05T10:48:00Z</timestamp>
            <telemetryDetails>
                <sensorCode>sensor8192</sensorCode>
                <value>45.6</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor8200</sensorCode>
                <value>85.5</value>
            </telemetryDetails>
        </web:submitData>
    </soapenv:Body>
</soapenv:Envelope>
```

### JSON Format
```json
{
    "unitId": "XG3780_DEVICE_001",
    "latitude": 40.7589,
    "longitude": -73.9851,
    "telemetryDetails": [
        {"sensorCode": "sensor8192", "value": "45.6"},
        {"sensorCode": "sensor8200", "value": "85.5"}
    ]
}
```

## Sensor Mapping System

### Boolean Sensors (sensor0 - sensor172)
| Sensor ID | Name | Description | Category |
|-----------|------|-------------|----------|
| sensor0 | SENSOR_IGNITION | Ignition Status | vehicle_status |
| sensor1 | SENSOR_MODEM_ON | GPS Valid/Modem Status | connectivity |
| sensor2 | SENSOR_SPEED_LIMIT | Speed Over Limit | vehicle_status |
| sensor3-6 | SENSOR_INPUT_1-4 | Digital Input Status | io |
| sensor7 | SENSOR_OUTPUT_1 | Digital Output Status | io |
| sensor8 | SENSOR_GSM_JAMMING | Panic Button/GSM Jamming | connectivity |
| sensor9 | SENSOR_GPS_JAMMING | GPS Jamming Detection | connectivity |
| sensor10 | SENSOR_LOW_POWER | Low Power Warning | power |

### Numeric Sensors (sensor8192+)

#### GPS and Movement (8192-8199)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8192 | SENSOR_GNSS_SPEED | km/h | GNSS Speed |
| sensor8193 | SENSOR_GNSS_COURSE | degrees | GNSS Heading |
| sensor8194 | SENSOR_GNSS_ALTITUDE | meters | GNSS Altitude |
| sensor8195 | SENSOR_GNSS_HDOP | - | Horizontal Dilution of Precision |
| sensor8196 | SENSOR_GNSS_SATELLITES | count | Number of Satellites |

#### Engine Monitoring (8200-8223)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8200 | SENSOR_ENGINE_TEMPERATURE | °C | Engine Coolant Temperature |
| sensor8201 | SENSOR_ENGINE_OIL_PRESSURE | kPa | Engine Oil Pressure |
| sensor8202 | SENSOR_ENGINE_OIL_TEMP | °C | Engine Oil Temperature |
| sensor8208 | SENSOR_ENGINE_RPM | rpm | Engine RPM |
| sensor8209 | SENSOR_VEHICLE_SPEED | km/h | Vehicle Speed (CAN) |
| sensor8210 | SENSOR_ACCELERATOR | % | Accelerator Pedal Position |

#### Fuel System (8224-8239)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8224 | SENSOR_FUEL_LEVEL | % | Fuel Level |
| sensor8225 | SENSOR_FUEL_RATE | L/h | Fuel Consumption Rate |

#### Power System (8240-8255)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8240 | SENSOR_BATTERY_VOLTAGE | V | Main Battery Voltage |
| sensor8241 | SENSOR_EXTERNAL_VOLTAGE | V | External Power Voltage |

#### Environmental (8256-8271)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8256 | SENSOR_AMBIENT_TEMP | °C | Ambient Temperature |
| sensor8257 | SENSOR_CABIN_TEMP | °C | Cabin Temperature |

#### Diagnostics (8272+)
| Sensor ID | Name | Unit | Description |
|-----------|------|------|-------------|
| sensor8272 | SENSOR_ENGINE_HOURS | hours | Total Engine Hours |
| sensor8273 | SENSOR_TOTAL_DISTANCE | km | Total Vehicle Distance |
| sensor8274 | SENSOR_HI_RES_DISTANCE | m | High Resolution Distance |

## Sensor Categories

The system automatically categorizes sensors for better organization:

- **GPS**: Location and movement sensors
- **Engine**: Engine performance and diagnostics
- **Fuel**: Fuel system monitoring
- **Power**: Battery and electrical system
- **Environmental**: Temperature and climate
- **Vehicle Status**: Operational status indicators
- **Connectivity**: Communication and signal status
- **I/O**: Digital inputs and outputs
- **CAN Bus**: Controller Area Network data
- **Other**: Uncategorized or unknown sensors

## Calibration System

Sensors are automatically calibrated based on Xirgo specifications:

```python
# Example calibration for Engine Temperature
sensor8200_raw_value = 85.5  # Raw ADC value
calibrated_value = (raw_value - 40) * 0.75  # Apply offset and multiplier
# Result: 34.125°C
```

Common calibration formulas:
- **Temperature sensors**: `(raw_value - offset) * multiplier`
- **Voltage sensors**: `raw_value * voltage_divider_ratio`
- **Pressure sensors**: `raw_value * pressure_scale_factor`

## Authentication

### WS-Security (SOAP)
```xml
<wsse:Security>
    <wsse:UsernameToken>
        <wsse:Username>your_webhook_token</wsse:Username>
    </wsse:UsernameToken>
</wsse:Security>
```

### Bearer Token
```
Authorization: Bearer your_webhook_token
```

### Query Parameter
```
POST /webhook/wialon?api_key=your_webhook_token
```

## API Response

Successful processing returns:
```json
{
    "status": "success",
    "processed_count": 1,
    "processing_time_ms": 45
}
```

## Webhook Endpoint

**URL**: `https://your-domain.com/webhook/wialon`
**Method**: `POST`
**Content-Type**: 
- `application/soap+xml` (recommended)
- `application/json`
- `application/xml`
- `application/x-www-form-urlencoded`

## Configuration

Set environment variables:
```bash
WEBHOOK_AUTH_TOKEN=your_secure_token
RATE_LIMIT_PER_MINUTE=100
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Testing

Use the included test script:
```bash
python test_telemetry.py
```

## Monitoring

- **Dashboard**: Real-time device and data statistics
- **Logs**: Detailed webhook processing logs with parsed telemetry
- **Live Messages**: Real-time webhook monitoring
- **Health Check**: `/health` endpoint for system monitoring

## Error Handling

The system handles:
- Invalid sensor codes (marked as SENSOR_UNKNOWN_XXXX)
- Missing calibration data (uses default values)
- Malformed XML/JSON (logs error, continues processing)
- Authentication failures (401 response)
- Rate limiting (429 response)

## Data Storage

Telemetry data is stored as structured JSON in the database:
```json
{
    "SENSOR_GNSS_SPEED": {
        "value": 45.6,
        "raw_value": "45.6",
        "unit": "km/h",
        "type": "numeric",
        "category": "gps",
        "sensor_id": 8192
    }
}
```

This enables efficient querying and analysis of sensor data while maintaining full traceability to original values.