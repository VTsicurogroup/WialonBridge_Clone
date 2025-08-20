# Wialon Retranslator Configuration

## Overview
This document provides the exact configuration parameters needed to set up your Wialon Retranslator to send data from Xirgo/Sensata XG3780 devices to this webhook receiver.

## Webhook Endpoint Configuration

### Required Parameters for Wialon Retranslator:

**Server:** `https://[your-replit-app-url].replit.app`
**Login:** `webhook_user` (or any identifier you prefer)
**Password:** `default_webhook_token`

### Complete Endpoint Details:

- **Full Webhook URL:** `https://[your-replit-app-url].replit.app/webhook/wialon`
- **HTTP Method:** POST
- **Authentication:** Bearer Token or API Key parameter
- **Supported Formats:** JSON, XML/SOAP, Form-encoded data
- **Rate Limit:** 100 requests per minute per IP address

## Authentication Options

You can authenticate your webhook requests in two ways:

### Option 1: Authorization Header (Recommended)
```
Authorization: Bearer default_webhook_token
```

### Option 2: URL Parameter
```
POST /webhook/wialon?api_key=default_webhook_token
```

## Wialon Retranslator Setup Steps

1. **Login to Wialon Interface**
   - Access your Wialon account
   - Navigate to Management → Retranslators

2. **Create New Retranslator**
   - Click "Create Retranslator"
   - Choose protocol: HTTP/HTTPS
   - Set destination server details

3. **Configure Server Settings**
   ```
   Protocol: HTTP(S)
   Server: [your-replit-app-url].replit.app
   Port: 443 (for HTTPS) or 80 (for HTTP)
   Path: /webhook/wialon
   ```

4. **Set Authentication**
   - Add custom header: `Authorization: Bearer default_webhook_token`
   - Or use URL parameter: `?api_key=default_webhook_token`

5. **Select Units**
   - Choose your Xirgo/Sensata XG3780 devices
   - Ensure each device has a unique unit ID

6. **Data Format Options**
   - JSON (recommended for modern integrations)
   - XML/SOAP (if required by your system)
   - Form-encoded (for simple setups)

## Expected Data Fields

The webhook will automatically parse and store the following data from your tracking devices:

### Location Data
- Latitude, Longitude, Altitude
- Speed, Heading/Course
- GPS validity status

### Vehicle Telemetry (Xirgo/Sensata XG3780 specific)
- Odometer readings
- Fuel level
- Engine hours
- Battery voltage
- External voltage
- Ignition status

### Timestamps
- Device timestamp (from GPS data)
- Server timestamp (when received)

## Testing Your Setup

### Health Check
Test if the webhook is accessible:
```bash
curl https://[your-replit-app-url].replit.app/health
```

### Sample Test Request
Send a test webhook request:
```bash
curl -X POST https://[your-replit-app-url].replit.app/webhook/wialon \
  -H "Authorization: Bearer default_webhook_token" \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": "TEST001",
    "lat": 40.7128,
    "lng": -74.0060,
    "speed": 25.5,
    "timestamp": "2025-01-01T12:00:00Z"
  }'
```

## Security Considerations

### Change Default Authentication Token
For production use, update the webhook authentication token:

1. Set environment variable: `WEBHOOK_AUTH_TOKEN=your_secure_token`
2. Update your Wialon retranslator configuration accordingly

### SSL/HTTPS
Always use HTTPS in production for secure data transmission.

### Rate Limiting
The system includes built-in rate limiting (100 requests/minute per IP). Contact support if you need higher limits.

## Monitoring and Troubleshooting

### Dashboard Access
- URL: `https://[your-replit-app-url].replit.app`
- Default login: `admin` / `admin123`
- Change default credentials after first login

### Webhook Logs
Monitor incoming requests in real-time:
- Dashboard → Logs section
- View request details, status codes, and error messages
- Filter by timestamp, endpoint, or status

### Device Management
Track registered devices:
- Dashboard → Devices section
- View device status, last seen timestamps
- Monitor data reception per device

## Support

If you encounter issues:
1. Check the webhook logs for error details
2. Verify authentication token matches
3. Ensure proper JSON/XML formatting
4. Test with the health check endpoint first

## API Reference

### Webhook Endpoint
- **URL:** `/webhook/wialon`
- **Method:** POST
- **Auth:** Required (Bearer token or api_key parameter)
- **Response:** JSON with processing status

### Health Check
- **URL:** `/health`
- **Method:** GET
- **Auth:** None required
- **Response:** System status and metrics