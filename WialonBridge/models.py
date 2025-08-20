from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Index

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.String(64), unique=True, nullable=False)
    device_type = db.Column(db.String(64), default='Xirgo/Sensata XG3780')
    name = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with tracking data
    tracking_data = db.relationship('TrackingData', backref='device', lazy=True)

class TrackingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    
    # Location data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)
    speed = db.Column(db.Float)
    heading = db.Column(db.Float)
    
    # Timestamp information
    timestamp = db.Column(db.DateTime, nullable=False)
    server_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Vehicle data specific to Xirgo devices
    odometer = db.Column(db.Float)
    fuel_level = db.Column(db.Float)
    engine_hours = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    external_voltage = db.Column(db.Float)
    
    # Status flags
    ignition_status = db.Column(db.Boolean)
    gps_valid = db.Column(db.Boolean, default=True)
    panic_button = db.Column(db.Boolean, default=False)
    
    # Structured telemetry data (JSON)
    telemetry_data = db.Column(db.Text)  # Store structured sensor data as JSON
    
    # Raw data for debugging
    raw_data = db.Column(db.Text)
    data_format = db.Column(db.String(32))  # json, xml, form
    
    # Index for performance
    __table_args__ = (
        Index('ix_tracking_data_device_timestamp', 'device_id', 'timestamp'),
        Index('ix_tracking_data_timestamp', 'timestamp'),
    )
    
    @property
    def telemetry(self):
        """Get parsed telemetry data as dict"""
        if self.telemetry_data:
            try:
                import json
                return json.loads(self.telemetry_data)
            except:
                return {}
        return {}
    
    def set_telemetry(self, telemetry_dict):
        """Set telemetry data from dict"""
        import json
        self.telemetry_data = json.dumps(telemetry_dict) if telemetry_dict else None

class WebhookLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    endpoint = db.Column(db.String(128), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    content_type = db.Column(db.String(128))
    content_length = db.Column(db.Integer)
    remote_addr = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))
    status_code = db.Column(db.Integer)
    processing_time_ms = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    request_data_sample = db.Column(db.Text)  # First 1000 chars of request data
    
    # Index for performance
    __table_args__ = (
        Index('ix_webhook_log_timestamp', 'timestamp'),
        Index('ix_webhook_log_endpoint', 'endpoint'),
    )

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    key_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)
