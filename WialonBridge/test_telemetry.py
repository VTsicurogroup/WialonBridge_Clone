#!/usr/bin/env python3
"""
Test script to verify telemetry mapping system with SOAP XML data
"""

import json
import requests
from datetime import datetime

def test_telemetry_mapping():
    """Test the telemetry mapping with sample SOAP XML data"""
    
    # Sample SOAP XML with telemetry details (simulating Wialon retranslator data)
    soap_xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservice.retranslator.wialon">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>default_webhook_token</wsse:Username>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        <web:submitData>
            <unitId>XG3780_TEST_001</unitId>
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
            <telemetryDetails>
                <sensorCode>sensor8208</sensorCode>
                <value>1250</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor8224</sensorCode>
                <value>12.6</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor8240</sensorCode>
                <value>24.3</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor0</sensorCode>
                <value>1</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor1</sensorCode>
                <value>0</value>
            </telemetryDetails>
            <telemetryDetails>
                <sensorCode>sensor8</sensorCode>
                <value>1</value>
            </telemetryDetails>
        </web:submitData>
    </soapenv:Body>
</soapenv:Envelope>'''
    
    # Test webhook endpoint locally
    webhook_url = "http://localhost:5000/webhook/wialon"
    
    headers = {
        'Content-Type': 'application/soap+xml',
        'SOAPAction': 'submitData'
    }
    
    print("Testing telemetry mapping with SOAP XML data...")
    print(f"Webhook URL: {webhook_url}")
    print(f"Sample sensors included:")
    print("- sensor8192: GNSS Speed")
    print("- sensor8200: Engine Coolant Temperature") 
    print("- sensor8208: Engine RPM")
    print("- sensor8224: Fuel Level")
    print("- sensor8240: Battery Voltage")
    print("- sensor0: Ignition Status (boolean)")
    print("- sensor1: GPS Valid (boolean)")
    print("- sensor8: Panic Button (boolean)")
    print()
    
    try:
        response = requests.post(webhook_url, data=soap_xml_data, headers=headers, timeout=10)
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ Webhook processed successfully!")
            print("Check the logs page at http://localhost:5000/logs to see the parsed telemetry data")
        else:
            print(f"\n❌ Webhook failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to webhook endpoint")
        print("Make sure the Flask application is running on port 5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_telemetry_mapping()