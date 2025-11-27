# Communal Collage Activity

A collaborative image collage application where users can upload images to a shared collection.

## Configuration

All configuration is centralized in `config.py` for easy management.

### Changing the Production URL

To change your cloud hosting URL (e.g., if you deploy to a different service), simply edit **one line** in `config.py`:

```python
PRODUCTION_URL = "https://your-new-url.com"
```

This will automatically update:
- CORS origins
- All references throughout the application

### Other Configuration Options

All settings can be found in `config.py`:
- `PRODUCTION_URL` - Your production deployment URL
- `LOCAL_PORT` - Local development port (default: 5001)
- `MAX_FILE_SIZE_MB` - Maximum upload size (default: 10MB)
- `ALLOWED_EXTENSIONS` - Allowed image file types
- MinIO settings (can also be set via environment variables)

## Environment Variables

You can override configuration using environment variables:
- `MINIO_ENDPOINT` - MinIO server endpoint
- `MINIO_ACCESS_KEY` - MinIO access key
- `MINIO_SECRET_KEY` - MinIO secret key
- `BASE_URL` - Override base URL
- `FLASK_ENV` - Set to 'production' for production mode