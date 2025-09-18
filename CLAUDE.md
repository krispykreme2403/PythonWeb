# PyDateNight - Claude Code Documentation

## Project Overview
Django application for finding date night restaurants using Yelp's GraphQL API.

## Development Setup
- **Virtual Environment**: `/home/thebaze/PythonWeb/venv/`
- **Activation**: `source venv/bin/activate`
- **Django Project**: `/home/thebaze/PythonWeb/PyDateNight/`

## Deployment
- **Development Server**: `python manage.py runserver 0.0.0.0:8000`
- **Production**: Apache2 with mod_wsgi
- **WSGI Reload**: `touch /home/thebaze/PythonWeb/PyDateNight/PyDateNight/wsgi.py`

## Known Issues & Solutions

### fetch_restaurants Endpoint 500 Errors
**Problem**: The `/fetch_restaurants/` endpoint was returning 500 errors

**Root Causes**:
1. **ALLOWED_HOSTS**: Missing localhost/127.0.0.1 in Django settings
2. **Yelp API Rate Limiting**: Too many concurrent requests (QPS limits)

**Solutions Applied**:
1. **Fixed ALLOWED_HOSTS** in `PyDateNight/settings.py`:
   ```python
   ALLOWED_HOSTS = ['20.168.121.122', 'localhost', '127.0.0.1']
   ```

2. **Optimized API Request Limits** in `home/yelp.py`:
   ```python
   max_requests = 5  # Conservative limit to prevent QPS rate limiting
   ```

### Yelp API Limits
- **Daily Limit**: 25,000 points per 24 hours
- **Business Node**: 10 points each
- **Current Config**: 250 businesses per run (2,500 points)
- **Daily Capacity**: ~10 runs maximum

### Troubleshooting Commands
```bash
# Check Django migrations
python manage.py check

# Test endpoint
curl http://localhost:8000/fetch_restaurants/

# Check Apache status
sudo systemctl status apache2

# Reload WSGI application
touch /home/thebaze/PythonWeb/PyDateNight/PyDateNight/wsgi.py
```

## API Endpoints
- `/` - Home page with restaurant alphabet navigation
- `/restaurant_list/` - Restaurant list view with filtering
- `/fetch_restaurants/` - Fetches new restaurant data from Yelp API

## Dependencies
- Django 5.2.6
- requests 2.32.5
- Bootstrap 5.3.3 (CDN)