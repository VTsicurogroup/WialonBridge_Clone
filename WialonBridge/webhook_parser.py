import json
import xml.etree.ElementTree as ET
import xmltodict
from datetime import datetime
from dateutil import parser as date_parser
import logging
from telemetry_mapping import (
    get_sensor_info, 
    apply_sensor_calibration, 
    parse_sensor_code,
    get_sensor_category,
    SENSOR_CATEGORIES
)

def parse_wialon_data(request):
    """
    Parse incoming Wialon retranslator data from various formats
    Returns a list of parsed data entries
    """
    content_type = request.content_type or ''
    parsed_data = []
    
    try:
        if 'application/json' in content_type:
            parsed_data = parse_json_data(request)
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            parsed_data = parse_xml_data(request)
        elif 'application/x-www-form-urlencoded' in content_type:
            parsed_data = parse_form_data(request)
        else:
            # Try to auto-detect format
            data = request.get_data(as_text=True)
            if data.strip().startswith('{') or data.strip().startswith('['):
                parsed_data = parse_json_data(request)
            elif data.strip().startswith('<'):
                parsed_data = parse_xml_data(request)
            else:
                parsed_data = parse_form_data(request)
                
    except Exception as e:
        logging.error(f"Error parsing webhook data: {e}")
        return []
    
    return parsed_data

def parse_json_data(request):
    """Parse JSON format data from Wialon retranslator"""
    try:
        data = request.get_json()
        if not data:
            return []
        
        parsed_entries = []
        
        # Handle single entry or array of entries
        if isinstance(data, list):
            entries = data
        else:
            entries = [data]
        
        for entry in entries:
            parsed_entry = extract_tracking_data(entry, 'json', json.dumps(entry))
            if parsed_entry:
                parsed_entries.append(parsed_entry)
        
        return parsed_entries
        
    except Exception as e:
        logging.error(f"Error parsing JSON data: {e}")
        return []

def parse_xml_data(request):
    """Parse XML/SOAP format data from Wialon retranslator"""
    try:
        xml_data = request.get_data(as_text=True)
        if not xml_data:
            return []
        
        # Convert XML to dict for easier processing
        parsed_xml = xmltodict.parse(xml_data)
        
        parsed_entries = []
        
        # Handle SOAP envelope with different namespace prefixes
        envelope_key = None
        body_key = None
        
        # Find envelope and body keys regardless of namespace prefix
        for key in parsed_xml.keys():
            if 'Envelope' in key:
                envelope_key = key
                break
        
        if envelope_key:
            envelope = parsed_xml[envelope_key]
            for key in envelope.keys():
                if 'Body' in key:
                    body_key = key
                    break
            
            if body_key:
                body = envelope[body_key]
                entries = extract_entries_from_soap(body)
            else:
                entries = [envelope]
        else:
            # Direct XML format
            entries = [parsed_xml]
        
        for entry in entries:
            parsed_entry = extract_tracking_data(entry, 'xml', xml_data[:1000])
            if parsed_entry:
                parsed_entries.append(parsed_entry)
        
        return parsed_entries
        
    except Exception as e:
        logging.error(f"Error parsing XML data: {e}")
        return []

def parse_form_data(request):
    """Parse form-encoded data from Wialon retranslator"""
    try:
        form_data = request.form.to_dict()
        if not form_data:
            return []
        
        parsed_entry = extract_tracking_data(form_data, 'form', str(form_data))
        if parsed_entry:
            return [parsed_entry]
        
        return []
        
    except Exception as e:
        logging.error(f"Error parsing form data: {e}")
        return []

def extract_entries_from_soap(soap_body):
    """Extract data entries from SOAP body"""
    entries = []
    
    def extract_telemetry_recursive(data):
        """Recursively search for telemetry data"""
        if isinstance(data, dict):
            # Check if this dict contains tracking data (GPS coordinates, unit ID, or telemetry details)
            has_tracking_data = any(key in data for key in [
                'coordX', 'coordY', 'gpsCode', 'latitude', 'longitude', 
                'unitId', 'unit_id', 'telemetryDetails', 'lat', 'lon'
            ])
            
            if has_tracking_data:
                entries.append(data)
            
            # Also search nested structures for additional data
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    extract_telemetry_recursive(value)
                    
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    extract_telemetry_recursive(item)
    
    # Start recursive search from SOAP body
    extract_telemetry_recursive(soap_body)
    
    return entries

def extract_tracking_data(data, data_format, raw_data):
    """
    Extract standardized tracking data from parsed entry
    Handles various field naming conventions from Wialon retranslator
    """
    try:
        # Initialize result
        result = {
            'data_format': data_format,
            'raw_data': raw_data
        }
        
        # Extract unit/device ID (various possible field names)
        unit_id = (data.get('unit_id') or 
                  data.get('unitId') or 
                  data.get('id') or 
                  data.get('device_id') or 
                  data.get('deviceId') or 
                  data.get('imei') or
                  data.get('uid') or
                  data.get('gpsCode') or    # Wialon specific
                  data.get('gps_code') or
                  data.get('code'))
        
        if not unit_id:
            logging.warning("No unit ID found in data entry")
            return None
        
        result['unit_id'] = str(unit_id)
        
        # Extract location data (Wialon uses coordX/coordY)
        result['latitude'] = safe_float(data.get('lat') or data.get('latitude') or data.get('y') or data.get('coordY'))
        result['longitude'] = safe_float(data.get('lon') or data.get('lng') or data.get('longitude') or data.get('x') or data.get('coordX'))
        result['altitude'] = safe_float(data.get('alt') or data.get('altitude') or data.get('z'))
        result['speed'] = safe_float(data.get('speed') or data.get('spd'))
        result['heading'] = safe_float(data.get('heading') or data.get('course') or data.get('dir'))
        
        # Extract timestamp (Wialon uses 'date' field)
        timestamp_fields = ['timestamp', 'time', 't', 'datetime', 'dt', 'server_time', 'date']
        timestamp = None
        
        for field in timestamp_fields:
            if field in data and data[field]:
                try:
                    if isinstance(data[field], (int, float)):
                        # Unix timestamp
                        timestamp = datetime.fromtimestamp(data[field])
                    else:
                        # Parse string timestamp
                        timestamp = date_parser.parse(str(data[field]))
                    break
                except:
                    continue
        
        result['timestamp'] = timestamp or datetime.utcnow()
        
        # Extract Xirgo/vehicle specific data
        result['odometer'] = safe_float(data.get('odometer') or data.get('mileage'))
        result['fuel_level'] = safe_float(data.get('fuel') or data.get('fuel_level'))
        result['engine_hours'] = safe_float(data.get('engine_hours') or data.get('hours'))
        result['battery_voltage'] = safe_float(data.get('battery') or data.get('battery_voltage'))
        result['external_voltage'] = safe_float(data.get('external_voltage') or data.get('ext_voltage'))
        
        # Extract status flags
        result['ignition_status'] = safe_bool(data.get('ignition') or data.get('ign'))
        result['gps_valid'] = safe_bool(data.get('gps_valid') or data.get('valid'), default=True)
        result['panic_button'] = safe_bool(data.get('panic') or data.get('sos'), default=False)
        
        # Extract telemetry details if present (from SOAP XML)
        telemetry_details = data.get('telemetryDetails', [])
        if telemetry_details:
            mapped_telemetry = {}
            
            # Handle both single detail and list of details
            if not isinstance(telemetry_details, list):
                telemetry_details = [telemetry_details]
            
            for detail in telemetry_details:
                sensor_code = detail.get('sensorCode')
                raw_value = detail.get('value')
                
                if sensor_code and raw_value is not None:
                    try:
                        # Import telemetry mapping functions
                        from telemetry_mapping import parse_sensor_code, get_sensor_info, apply_sensor_calibration, get_sensor_category
                        
                        # Parse and map sensor code to Xirgo specification
                        sensor_id = parse_sensor_code(sensor_code)
                        if sensor_id:
                            sensor_info = get_sensor_info(sensor_id)
                            
                            # Apply calibration (multiplier and offset)
                            calibrated_value = apply_sensor_calibration(sensor_id, raw_value)
                            
                            # Store mapped telemetry with sensor info
                            mapped_telemetry[sensor_info['name']] = {
                                'value': calibrated_value,
                                'raw_value': raw_value,
                                'unit': sensor_info['unit'],
                                'type': sensor_info['type'],
                                'category': get_sensor_category(sensor_info['name']),
                                'sensor_id': sensor_id
                            }
                    except Exception as e:
                        # Log error but continue processing
                        print(f"Error processing sensor {sensor_code}: {e}")
                        continue
            
            if mapped_telemetry:
                result['telemetry'] = mapped_telemetry
        
        # Extract sensor data if present (for other formats)
        if 'sensors' in data:
            sensors = data['sensors']
            if isinstance(sensors, dict):
                for sensor_id, sensor_value in sensors.items():
                    # Map common sensor IDs to fields
                    if 'fuel' in str(sensor_id).lower():
                        result['fuel_level'] = safe_float(sensor_value)
                    elif 'temp' in str(sensor_id).lower():
                        # Could add temperature fields if needed
                        pass
        
        return result
        
    except Exception as e:
        logging.error(f"Error extracting tracking data: {e}")
        return None

def safe_float(value):
    """Safely convert value to float, return None if not possible"""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_bool(value, default=False):
    """Safely convert value to boolean"""
    if value is None:
        return default
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, (int, float)):
        return bool(value)
    
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on', 'active')
    
    return default
