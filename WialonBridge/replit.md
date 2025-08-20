# Overview

This is a Flask web application designed to receive and process tracking data from Wialon retranslator webhooks, specifically targeting Xirgo/Sensata XG3780 GPS tracking devices. The system provides a web dashboard for monitoring devices, viewing tracking data, and analyzing webhook logs with real-time updates and visualization capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask**: Core web framework with modular blueprint architecture
- **SQLAlchemy ORM**: Database abstraction layer with declarative models
- **Flask-Login**: Session-based authentication system with user management

## Database Design
- **SQLite/PostgreSQL**: Configurable database backend (defaults to SQLite for development)
- **Three-tier data model**:
  - User management (authentication, admin roles)
  - Device registry (unit tracking, status monitoring)
  - Tracking data storage (GPS coordinates, vehicle telemetry)
- **Optimized for time-series data** with proper indexing for tracking queries

## Authentication & Security
- **Password-based authentication** with hashed storage using Werkzeug
- **Session management** via Flask-Login with remember-me functionality
- **Role-based access control** with admin user capabilities
- **Rate limiting** for webhook endpoints (100 requests/minute default)

## Webhook Processing
- **Multi-format parser** supporting JSON, XML, and form-encoded data
- **Automatic format detection** for flexible data ingestion
- **Request logging and monitoring** with performance metrics
- **Error handling and validation** for malformed data

## Frontend Architecture
- **Bootstrap 5** with dark theme for responsive UI
- **Feather Icons** for consistent iconography
- **Chart.js** for real-time data visualization
- **Template inheritance** using Jinja2 for maintainable views

## Data Processing Pipeline
- **Real-time webhook ingestion** with immediate database storage
- **Device auto-registration** when new unit IDs are detected
- **Timestamp handling** with both device and server timestamps
- **Telemetry extraction** including GPS, fuel, engine hours, and voltage data

# External Dependencies

## Core Framework Dependencies
- **Flask ecosystem**: SQLAlchemy, Login, security extensions
- **Database drivers**: PostgreSQL adapter (configurable)
- **Date/time processing**: dateutil for flexible timestamp parsing
- **HTTP requests**: requests library for testing and external API calls

## Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme support
- **Chart.js**: Real-time charting and visualization
- **Feather Icons**: SVG icon library
- **Moment.js**: Client-side date/time manipulation

## Development Tools
- **Werkzeug**: WSGI utilities and development server
- **ProxyFix**: Production deployment support for reverse proxies
- **XML processing**: ElementTree and xmltodict for multi-format parsing

## Telemetry Processing
- **Comprehensive sensor mapping**: 172 boolean + 8192+ numeric sensors for Xirgo/Sensata XG3780
- **Automatic calibration**: Sensor value conversion with multipliers and offsets
- **Structured data storage**: JSON-based telemetry storage with categorization
- **SOAP XML parsing**: Full WS-Security authentication support
- **Real-time telemetry display**: Enhanced UI showing categorized sensor data with units

## Configuration Dependencies
- **Environment variables**: Database URL, webhook tokens, rate limits
- **Session management**: Configurable secret keys for security
- **Logging system**: Python's built-in logging with debug capabilities