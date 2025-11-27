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

## Docker Deployment

### Quick Start (Detached Mode)

Run the application in detached mode using Docker Compose:

```bash
# Using the convenience script
./docker-run.sh

# Or manually
docker-compose up -d --build
```

This will start both the Flask app and MinIO in detached mode.

### Docker Commands

```bash
# Start containers in detached mode
docker-compose up -d

# View logs
docker-compose logs -f app        # Flask app logs
docker-compose logs -f minio      # MinIO logs
docker-compose logs -f            # All logs

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# Rebuild and restart
docker-compose up -d --build

# Check container status
docker-compose ps
```

### Access Points

- **Flask Application**: http://localhost:5001
- **MinIO Admin Console**: http://localhost:9001
  - Username: `admin`
  - Password: `password123`

### Building Docker Image Only

If you want to build just the Docker image:

```bash
docker build -t communal-collage-app .
docker run -d -p 5001:5001 --name communal-collage communal-collage-app
```

### Docker Compose Services

- **app**: Flask application (port 5001)
- **minio**: MinIO object storage (ports 9000, 9001)

Both services are configured to restart automatically and run in detached mode.