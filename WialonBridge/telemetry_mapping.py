"""
Xirgo/Sensata XG3780 Telemetry Sensor Mapping
Based on Xirgo Global documentation: https://docs.xirgoglobal.com/space/SD/27149650/Sensor+properties
"""

# Sensor mapping from Xirgo documentation
XIRGO_SENSOR_MAP = {
    # Digital/Boolean Sensors (0-172)
    1: {'name': 'SENSOR_MODEM_ON', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    2: {'name': 'SENSOR_MOTION_DETECTED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    5: {'name': 'SENSOR_SYSTEM_TIME_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    6: {'name': 'SENSOR_INSIDE_GEOZONE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    7: {'name': 'SENSOR_POOR_GNSS_SIGNAL', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    8: {'name': 'SENSOR_GSM_JAMMING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    9: {'name': 'SENSOR_ROAMING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    10: {'name': 'SENSOR_GSM_REGISTERED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    11: {'name': 'SENSOR_GPRS_REGISTERED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    12: {'name': 'SENSOR_PDP_ACTIVE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    13: {'name': 'SENSOR_PREFERRED_OPERATOR_ACTIVE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    14: {'name': 'SENSOR_GNSS_SPEED_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    15: {'name': 'SENSOR_SIGNAL_WIEGAND_ID_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    16: {'name': 'SENSOR_IN_2', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    17: {'name': 'SENSOR_IN_3', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    18: {'name': 'SENSOR_IN_4', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    19: {'name': 'SENSOR_IN_5', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    20: {'name': 'SENSOR_IN_7', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    21: {'name': 'SENSOR_IN_8', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    30: {'name': 'SENSOR_IBUTTON_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Vehicle CAN Bus Sensors
    96: {'name': 'SENSOR_ARMED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    97: {'name': 'SENSOR_LOCKED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    98: {'name': 'SENSOR_DOORS_F_L', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    99: {'name': 'SENSOR_DOORS_F_R', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    100: {'name': 'SENSOR_DOORS_R_L', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    101: {'name': 'SENSOR_DOORS_R_R', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    102: {'name': 'SENSOR_BONNET', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    103: {'name': 'SENSOR_TRUNK', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    108: {'name': 'SENSOR_FACTORY_ALARM', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    109: {'name': 'SENSOR_IGNITION', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Warning Indicators
    116: {'name': 'SENSOR_STOP_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    117: {'name': 'SENSOR_OIL_PRESSURE_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    118: {'name': 'SENSOR_COOLANT_FLUID_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    119: {'name': 'SENSOR_BRAKE_SYSTEM_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    120: {'name': 'SENSOR_BATTERY_VOLTAGE_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    121: {'name': 'SENSOR_AIRBAG_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    122: {'name': 'SENSOR_CHECK_ENGINE_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    123: {'name': 'SENSOR_HEADLAMP_MALFUNCTION_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    124: {'name': 'SENSOR_TIRE_PRESSURE_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    125: {'name': 'SENSOR_LOW_BRAKE_PAD_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    126: {'name': 'SENSOR_MASTER_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    127: {'name': 'SENSOR_ABS_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    128: {'name': 'SENSOR_LOW_FUEL_LEVEL_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    129: {'name': 'SENSOR_ESP_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    130: {'name': 'SENSOR_GLOW_PLUG_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    131: {'name': 'SENSOR_DPF_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    132: {'name': 'SENSOR_EPC_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    133: {'name': 'SENSOR_DRIVER_SEATBELT_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    134: {'name': 'SENSOR_PASSENGER_SEATBELT_WARNING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Status Indicators
    135: {'name': 'SENSOR_PARKING_LIGHT_INDICATOR', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    136: {'name': 'SENSOR_HEADLIGHT_INDICATOR', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    137: {'name': 'SENSOR_HIGH_BEAM_LIGHT_INDICATOR', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    138: {'name': 'SENSOR_KEY_INSERTED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    139: {'name': 'SENSOR_HANDBRAKE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    140: {'name': 'SENSOR_FOOT_BRAKE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    141: {'name': 'SENSOR_ENGINE_WORKING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    142: {'name': 'SENSOR_READY_TO_DRIVE', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    143: {'name': 'SENSOR_CRUISE_CONTROL', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    144: {'name': 'SENSOR_RETARDER_AUTO', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    145: {'name': 'SENSOR_RETARDER_MANUAL', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    146: {'name': 'SENSOR_AIR_CONDITIONING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    147: {'name': 'SENSOR_WEBASTO', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Output Controls
    148: {'name': 'SENSOR_OUT_1', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    149: {'name': 'SENSOR_OUT_2', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    150: {'name': 'SENSOR_OUT_3', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    154: {'name': 'SENSOR_OUT_4', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Motion/Security Sensors
    151: {'name': 'SENSOR_OVERTURN', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    152: {'name': 'SENSOR_SHOCK_1', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    153: {'name': 'SENSOR_SHOCK_2', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    155: {'name': 'SENSOR_GNSS_JAMMING', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    156: {'name': 'SENSOR_TAMPER', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Additional CAN Sensors
    157: {'name': 'SENSOR_CLUTCH_PEDAL_PRESSED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    158: {'name': 'SENSOR_PTO_ENABLED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    159: {'name': 'SENSOR_CAN_ACTIVITY_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    167: {'name': 'SENSOR_EXTERNAL_POWER_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    170: {'name': 'SENSOR_DTC_CAPTURED', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    171: {'name': 'SENSOR_CAN_1_ACTIVITY_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    172: {'name': 'SENSOR_CAN_2_ACTIVITY_PRESENT', 'type': 'bool', 'unit': '', 'multiplier': 1, 'offset': 0},
    
    # Analog/Numeric Sensors (8192+)
    8192: {'name': 'SENSOR_GNSS_SPEED', 'type': 'numeric', 'unit': 'km/h', 'multiplier': 1, 'offset': 0},
    8193: {'name': 'SENSOR_GNSS_SATELLITES', 'type': 'numeric', 'unit': '', 'multiplier': 1, 'offset': 0},
    8194: {'name': 'SENSOR_GNSS_H_DOP', 'type': 'numeric', 'unit': '', 'multiplier': 0.1, 'offset': 0},
    8195: {'name': 'SENSOR_MOBILE_NETWORK_CODE', 'type': 'numeric', 'unit': '', 'multiplier': 1, 'offset': 0},
    8196: {'name': 'SENSOR_TIMING_ADVANCE', 'type': 'numeric', 'unit': '', 'multiplier': 1, 'offset': 0},
    8197: {'name': 'SENSOR_GSM_POWER', 'type': 'numeric', 'unit': 'dBm', 'multiplier': 1, 'offset': 0},
    8198: {'name': 'SENSOR_PEDAL_POSITION', 'type': 'numeric', 'unit': '%', 'multiplier': 0.4, 'offset': 0},
    8199: {'name': 'SENSOR_FUEL_LEVEL_1', 'type': 'numeric', 'unit': '%/L', 'multiplier': 1, 'offset': 0},
    8200: {'name': 'SENSOR_ENGINE_TEMPERATURE', 'type': 'numeric', 'unit': '°C', 'multiplier': 1, 'offset': -40},
    8201: {'name': 'SENSOR_FUEL_LEVEL_2', 'type': 'numeric', 'unit': '%', 'multiplier': 1, 'offset': 0},
    8202: {'name': 'SENSOR_ENGINE_LOAD', 'type': 'numeric', 'unit': '%', 'multiplier': 1, 'offset': 0},
}

# Additional sensor categories for UI organization
SENSOR_CATEGORIES = {
    'gps': ['SENSOR_GNSS_SPEED', 'SENSOR_GNSS_SATELLITES', 'SENSOR_GNSS_H_DOP', 'SENSOR_GNSS_SPEED_PRESENT', 'SENSOR_POOR_GNSS_SIGNAL', 'SENSOR_GNSS_JAMMING'],
    'connectivity': ['SENSOR_MODEM_ON', 'SENSOR_GSM_REGISTERED', 'SENSOR_GPRS_REGISTERED', 'SENSOR_PDP_ACTIVE', 'SENSOR_GSM_JAMMING', 'SENSOR_ROAMING', 'SENSOR_GSM_POWER', 'SENSOR_MOBILE_NETWORK_CODE'],
    'engine': ['SENSOR_IGNITION', 'SENSOR_ENGINE_WORKING', 'SENSOR_ENGINE_TEMPERATURE', 'SENSOR_ENGINE_LOAD', 'SENSOR_PEDAL_POSITION', 'SENSOR_FUEL_LEVEL_1', 'SENSOR_FUEL_LEVEL_2'],
    'doors': ['SENSOR_DOORS_F_L', 'SENSOR_DOORS_F_R', 'SENSOR_DOORS_R_L', 'SENSOR_DOORS_R_R', 'SENSOR_BONNET', 'SENSOR_TRUNK', 'SENSOR_LOCKED'],
    'warnings': ['SENSOR_STOP_WARNING', 'SENSOR_OIL_PRESSURE_WARNING', 'SENSOR_COOLANT_FLUID_WARNING', 'SENSOR_BRAKE_SYSTEM_WARNING', 'SENSOR_BATTERY_VOLTAGE_WARNING', 'SENSOR_AIRBAG_WARNING', 'SENSOR_CHECK_ENGINE_WARNING'],
    'safety': ['SENSOR_SEATBELT_WARNING', 'SENSOR_HANDBRAKE', 'SENSOR_FOOT_BRAKE', 'SENSOR_CRUISE_CONTROL', 'SENSOR_ABS_WARNING', 'SENSOR_ESP_WARNING'],
    'security': ['SENSOR_ARMED', 'SENSOR_FACTORY_ALARM', 'SENSOR_MOTION_DETECTED', 'SENSOR_SHOCK_1', 'SENSOR_SHOCK_2', 'SENSOR_OVERTURN', 'SENSOR_TAMPER'],
    'lighting': ['SENSOR_PARKING_LIGHT_INDICATOR', 'SENSOR_HEADLIGHT_INDICATOR', 'SENSOR_HIGH_BEAM_LIGHT_INDICATOR', 'SENSOR_HEADLAMP_MALFUNCTION_WARNING'],
    'inputs': ['SENSOR_IN_2', 'SENSOR_IN_3', 'SENSOR_IN_4', 'SENSOR_IN_5', 'SENSOR_IN_7', 'SENSOR_IN_8'],
    'outputs': ['SENSOR_OUT_1', 'SENSOR_OUT_2', 'SENSOR_OUT_3', 'SENSOR_OUT_4'],
    'power': ['SENSOR_EXTERNAL_POWER_PRESENT', 'SENSOR_BATTERY_VOLTAGE_WARNING'],
    'comfort': ['SENSOR_AIR_CONDITIONING', 'SENSOR_WEBASTO', 'SENSOR_KEY_INSERTED'],
}

def get_sensor_info(sensor_id):
    """Get sensor information by ID"""
    return XIRGO_SENSOR_MAP.get(sensor_id, {
        'name': f'SENSOR_UNKNOWN_{sensor_id}',
        'type': 'unknown',
        'unit': '',
        'multiplier': 1,
        'offset': 0
    })

def apply_sensor_calibration(sensor_id, raw_value):
    """Apply multiplier and offset calibration to raw sensor value"""
    sensor_info = get_sensor_info(sensor_id)
    try:
        raw_val = float(raw_value)
        calibrated = (raw_val * sensor_info['multiplier']) + sensor_info['offset']
        return calibrated
    except (ValueError, TypeError):
        return raw_value

def get_sensor_category(sensor_name):
    """Get the category for a sensor name"""
    for category, sensors in SENSOR_CATEGORIES.items():
        if sensor_name in sensors:
            return category
    return 'other'

def parse_sensor_code(sensor_code):
    """Parse sensor code from XML to extract sensor ID"""
    if isinstance(sensor_code, str):
        if sensor_code.startswith('sensor'):
            try:
                sensor_id = int(sensor_code.replace('sensor', ''))
                return sensor_id
            except ValueError:
                pass
    return None