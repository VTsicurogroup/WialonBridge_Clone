from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models import Device, TrackingData, WebhookLog, ApiKey
from webhook_parser import parse_wialon_data
from datetime import datetime, timedelta
import time
import logging
import hashlib
import json

# Rate limiting storage (in production, use Redis)
rate_limit_storage = {}

def check_rate_limit(ip_address):
    """Simple rate limiting implementation"""
    current_time = time.time()
    minute_key = f"{ip_address}:{int(current_time // 60)}"
    
    if minute_key not in rate_limit_storage:
        rate_limit_storage[minute_key] = 0
    
    rate_limit_storage[minute_key] += 1
    
    # Clean old entries
    for key in list(rate_limit_storage.keys()):
        if int(key.split(':')[1]) < int(current_time // 60) - 5:
            del rate_limit_storage[key]
    
    return rate_limit_storage[minute_key] <= app.config["RATE_LIMIT_PER_MINUTE"]

def log_webhook_request(endpoint, method, status_code, processing_time_ms, error_message=None, request_data_sample=None):
    """Log webhook request for monitoring"""
    log_entry = WebhookLog(
        endpoint=endpoint,
        method=method,
        content_type=request.content_type,
        content_length=request.content_length,
        remote_addr=request.remote_addr,
        user_agent=request.headers.get('User-Agent', ''),
        status_code=status_code,
        processing_time_ms=processing_time_ms,
        error_message=error_message,
        request_data_sample=request_data_sample
    )
    db.session.add(log_entry)
    try:
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to log webhook request: {e}")

def authenticate_webhook(auth_header, api_key_param, soap_xml_data=None):
    """Authenticate webhook request"""
    webhook_token = app.config["WEBHOOK_AUTH_TOKEN"]
    
    # Check SOAP WS-Security authentication first
    if soap_xml_data:
        try:
            import xml.etree.ElementTree as ET
            
            # Parse the SOAP XML
            root = ET.fromstring(soap_xml_data)
            
            # Look for wsse:Username in the SOAP header
            namespaces = {
                'wsse': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd',
                'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'
            }
            
            username_elem = root.find('.//wsse:Username', namespaces)
            if username_elem is not None and username_elem.text == webhook_token:
                return True
                
        except Exception as e:
            logging.debug(f"SOAP authentication parsing error: {e}")
    
    # Check Authorization header
    if auth_header:
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            if token == webhook_token:
                return True
        elif auth_header.startswith('Token '):
            token = auth_header[6:]
            if token == webhook_token:
                return True
        elif auth_header.startswith('Basic '):
            # Some systems send Basic auth with token as username
            import base64
            try:
                decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
                if ':' in decoded:
                    username, password = decoded.split(':', 1)
                    if username == webhook_token or password == webhook_token:
                        return True
                elif decoded == webhook_token:
                    return True
            except:
                pass
        # Direct token in authorization header
        elif auth_header == webhook_token:
            return True
    
    # Check API key parameter
    if api_key_param and api_key_param == webhook_token:
        return True
    
    # Check for token in various parameter names
    for param_name in ['token', 'auth_token', 'webhook_token', 'password']:
        param_value = request.args.get(param_name) or request.form.get(param_name)
        if param_value == webhook_token:
            return True
    
    return False

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics for dashboard
    total_devices = Device.query.count()
    active_devices = Device.query.filter_by(is_active=True).count()
    
    # Recent tracking data (last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_data_count = TrackingData.query.filter(TrackingData.timestamp >= yesterday).count()
    
    # Recent webhook requests
    recent_webhooks = WebhookLog.query.order_by(WebhookLog.timestamp.desc()).limit(10).all()
    
    # Device activity (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    device_activity = db.session.query(Device.unit_id, db.func.count(TrackingData.id).label('count'))\
        .join(TrackingData)\
        .filter(TrackingData.timestamp >= week_ago)\
        .group_by(Device.unit_id)\
        .order_by(db.func.count(TrackingData.id).desc())\
        .limit(10).all()
    
    return render_template('dashboard.html',
                         total_devices=total_devices,
                         active_devices=active_devices,
                         recent_data_count=recent_data_count,
                         recent_webhooks=recent_webhooks,
                         device_activity=device_activity)

@app.route('/devices')
@login_required
def devices():
    from datetime import datetime
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    devices = Device.query.order_by(Device.last_seen.desc().nullslast(), Device.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('devices.html', devices=devices, datetime=datetime)

@app.route('/device/<int:device_id>/edit', methods=['POST'])
@login_required
def edit_device(device_id):
    """Edit device name"""
    device = Device.query.get_or_404(device_id)
    
    new_name = request.form.get('name', '').strip()
    if not new_name:
        flash('Device name cannot be empty', 'error')
        return redirect(url_for('devices'))
    
    device.name = new_name
    db.session.commit()
    
    flash(f'Device name updated to "{new_name}"', 'success')
    return redirect(url_for('devices'))

@app.route('/logs')
@login_required
def logs():
    """Display webhook logs with parsed data"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    logs = WebhookLog.query.order_by(WebhookLog.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # Get associated tracking data for each successful log entry
    logs_with_data = []
    for log in logs.items:
        # Find tracking data created around the same time as this webhook
        from datetime import timedelta
        time_window = timedelta(seconds=30)  # 30-second window
        
        tracking_data = TrackingData.query.filter(
            TrackingData.timestamp >= log.timestamp - time_window,
            TrackingData.timestamp <= log.timestamp + time_window
        ).all()
        
        # Parse telemetry data for each tracking entry
        for td in tracking_data:
            td.parsed_telemetry = td.telemetry  # Use the property to get parsed telemetry
        
        logs_with_data.append({
            'log': log,
            'tracking_data': tracking_data
        })
    
    # Create pagination-like object with the enhanced data
    class EnhancedPagination:
        def __init__(self, original_pagination, enhanced_items):
            self.items = enhanced_items
            self.page = original_pagination.page
            self.pages = original_pagination.pages
            self.per_page = original_pagination.per_page
            self.total = original_pagination.total
            self.has_prev = original_pagination.has_prev
            self.has_next = original_pagination.has_next
            self.prev_num = original_pagination.prev_num
            self.next_num = original_pagination.next_num
            self._original = original_pagination
        
        def iter_pages(self, *args, **kwargs):
            """Delegate iter_pages to original pagination"""
            return self._original.iter_pages(*args, **kwargs)
    
    enhanced_logs = EnhancedPagination(logs, logs_with_data)
    
    return render_template('logs.html', logs=enhanced_logs)

@app.route('/map')
@login_required
def map_view():
    """Display interactive map with device locations"""
    # Get latest location for each device
    subquery = db.session.query(
        TrackingData.device_id,
        db.func.max(TrackingData.timestamp).label('max_timestamp')
    ).filter(
        TrackingData.latitude.isnot(None),
        TrackingData.longitude.isnot(None)
    ).group_by(TrackingData.device_id).subquery()
    
    latest_locations = db.session.query(TrackingData)\
        .join(Device)\
        .join(subquery, 
              db.and_(TrackingData.device_id == subquery.c.device_id,
                     TrackingData.timestamp == subquery.c.max_timestamp))\
        .all()
    
    # Prepare data for map
    map_data = []
    for tracking in latest_locations:
        # Parse telemetry data
        telemetry_info = {}
        if tracking.telemetry:
            for sensor_name, sensor_data in tracking.telemetry.items():
                if sensor_data.get('category') in ['gps', 'engine', 'fuel', 'power']:
                    telemetry_info[sensor_name] = sensor_data
        
        map_data.append({
            'device_id': tracking.device.id,
            'unit_id': tracking.device.unit_id,
            'device_name': tracking.device.name or tracking.device.unit_id,
            'latitude': float(tracking.latitude),
            'longitude': float(tracking.longitude),
            'speed': tracking.speed or 0,
            'heading': tracking.heading or 0,
            'timestamp': tracking.timestamp.isoformat(),
            'is_active': tracking.device.is_active,
            'telemetry': telemetry_info
        })
    
    return render_template('map.html', map_data=map_data)

@app.route('/live-messages')
@login_required
def live_messages():
    """Live webhook message viewer"""
    from datetime import datetime, timedelta
    
    # Statistics for last 5 minutes
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    
    total_recent = WebhookLog.query.filter(WebhookLog.timestamp >= five_minutes_ago).count()
    successful = WebhookLog.query.filter(
        WebhookLog.timestamp >= five_minutes_ago, 
        WebhookLog.status_code == 200
    ).count()
    failed = total_recent - successful
    
    # Recent tracking data points
    data_points = TrackingData.query.filter(TrackingData.timestamp >= five_minutes_ago).count()
    
    stats = {
        'total_recent': total_recent,
        'successful': successful,
        'failed': failed,
        'data_points': data_points
    }
    
    # Recent messages (last 20)
    recent_messages = WebhookLog.query.order_by(WebhookLog.timestamp.desc()).limit(20).all()
    
    # Recent tracking data (last 10)
    recent_tracking = TrackingData.query.order_by(TrackingData.timestamp.desc()).limit(10).all()
    
    return render_template('live_messages.html', 
                         stats=stats,
                         recent_messages=recent_messages,
                         recent_tracking=recent_tracking)

@app.route('/webhook-data/<int:log_id>')
@login_required
def webhook_data(log_id):
    """View full raw webhook data"""
    log_entry = WebhookLog.query.get_or_404(log_id)
    return render_template('webhook_data.html', log_entry=log_entry)

# Webhook endpoints
@app.route('/webhook/wialon', methods=['POST'])
def wialon_webhook():
    start_time = time.time()
    
    # Rate limiting
    if not check_rate_limit(request.remote_addr):
        log_webhook_request('/webhook/wialon', 'POST', 429, 0, "Rate limit exceeded")
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    # Authentication with detailed logging
    auth_header = request.headers.get('Authorization')
    api_key = request.args.get('api_key') or request.form.get('api_key')
    
    # Log authentication details for debugging
    auth_debug = f"Auth header: {auth_header}, API key: {api_key}, All headers: {dict(request.headers)}"
    
    # Get SOAP XML data for authentication
    soap_xml_data = None
    if request.content_type and 'soap+xml' in request.content_type:
        soap_xml_data = request.get_data(as_text=True)
    
    # Check authentication including SOAP WS-Security
    if not authenticate_webhook(auth_header, api_key, soap_xml_data):
        processing_time = int((time.time() - start_time) * 1000)
        log_webhook_request('/webhook/wialon', 'POST', 401, processing_time, f"Authentication failed. {auth_debug}")
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        # Get request data sample for logging (increased limit for SOAP XML)
        request_data_sample = ""
        if request.data:
            request_data_sample = request.data.decode('utf-8', errors='ignore')[:5000]  # Increased to 5000 chars
        elif request.form:
            request_data_sample = str(dict(request.form))[:5000]
        
        # Parse the incoming data
        parsed_data = parse_wialon_data(request)
        
        if not parsed_data:
            processing_time = int((time.time() - start_time) * 1000)
            log_webhook_request('/webhook/wialon', 'POST', 400, processing_time, 
                              "No valid data found in request", request_data_sample)
            return jsonify({"error": "No valid data found"}), 400
        
        # Process each data entry
        processed_count = 0
        for data_entry in parsed_data:
            try:
                # Get or create device
                device = Device.query.filter_by(unit_id=data_entry['unit_id']).first()
                if not device:
                    device = Device(
                        unit_id=data_entry['unit_id'],
                        name=f"Device {data_entry['unit_id']}",
                        device_type='Xirgo/Sensata XG3780'
                    )
                    db.session.add(device)
                    db.session.flush()  # Get the ID
                
                # Update device last seen
                device.last_seen = datetime.utcnow()
                device.is_active = True
                
                # Create tracking data entry
                tracking_data = TrackingData(
                    device_id=device.id,
                    latitude=data_entry.get('latitude'),
                    longitude=data_entry.get('longitude'),
                    altitude=data_entry.get('altitude'),
                    speed=data_entry.get('speed'),
                    heading=data_entry.get('heading'),
                    timestamp=data_entry.get('timestamp', datetime.utcnow()),
                    odometer=data_entry.get('odometer'),
                    fuel_level=data_entry.get('fuel_level'),
                    engine_hours=data_entry.get('engine_hours'),
                    battery_voltage=data_entry.get('battery_voltage'),
                    external_voltage=data_entry.get('external_voltage'),
                    ignition_status=data_entry.get('ignition_status'),
                    gps_valid=data_entry.get('gps_valid', True),
                    panic_button=data_entry.get('panic_button', False),
                    raw_data=data_entry.get('raw_data'),
                    data_format=data_entry.get('data_format')
                )
                
                # Save structured telemetry data if present
                if 'telemetry' in data_entry:
                    tracking_data.telemetry_data = json.dumps(data_entry['telemetry'])
                
                db.session.add(tracking_data)
                processed_count += 1
                
            except Exception as e:
                logging.error(f"Error processing data entry: {e}")
                continue
        
        db.session.commit()
        
        processing_time = int((time.time() - start_time) * 1000)
        log_webhook_request('/webhook/wialon', 'POST', 200, processing_time, 
                          None, request_data_sample)
        
        return jsonify({
            "status": "success",
            "processed_count": processed_count,
            "processing_time_ms": processing_time
        }), 200
        
    except Exception as e:
        db.session.rollback()
        processing_time = int((time.time() - start_time) * 1000)
        error_message = str(e)
        logging.error(f"Webhook processing error: {error_message}")
        
        log_webhook_request('/webhook/wialon', 'POST', 500, processing_time, 
                          error_message, request_data_sample)
        
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute(db.text('SELECT 1'))
        
        # Check recent activity
        recent_webhooks = WebhookLog.query.filter(
            WebhookLog.timestamp >= datetime.utcnow() - timedelta(minutes=5)
        ).count()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "recent_webhooks": recent_webhooks
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

# Test endpoint without authentication for debugging
@app.route('/webhook/wialon/test', methods=['POST'])
def wialon_webhook_test():
    """Test endpoint to capture Wialon data without authentication"""
    start_time = time.time()
    
    try:
        # Get request data sample for logging
        request_data_sample = ""
        if request.data:
            request_data_sample = request.data.decode('utf-8', errors='ignore')[:1000]
        elif request.form:
            request_data_sample = str(dict(request.form))[:1000]
        
        # Log the test request with full details
        log_entry = WebhookLog(
            endpoint='/webhook/wialon/test',
            method='POST',
            content_type=request.content_type,
            content_length=request.content_length,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            status_code=200,
            processing_time_ms=int((time.time() - start_time) * 1000),
            error_message=f"TEST: Headers: {dict(request.headers)}",
            request_data_sample=request_data_sample
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            "status": "test_success",
            "message": "Data captured for analysis",
            "content_type": request.content_type,
            "content_length": request.content_length,
            "headers": dict(request.headers)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API endpoints for AJAX requests
@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    """Get real-time dashboard statistics"""
    try:
        # Get stats for the last hour
        hour_ago = datetime.utcnow() - timedelta(hours=1)
        
        hourly_data = db.session.query(
            db.func.strftime('%H', TrackingData.timestamp).label('hour'),
            db.func.count(TrackingData.id).label('count')
        ).filter(
            TrackingData.timestamp >= hour_ago
        ).group_by(
            db.func.strftime('%H', TrackingData.timestamp)
        ).all()
        
        return jsonify({
            "hourly_data": [{"hour": row.hour, "count": row.count} for row in hourly_data]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
