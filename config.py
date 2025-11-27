
# Configuration file for Communal Collage Activity
# Change the PRODUCTION_URL here to update it everywhere in the application

import os

# ============================================================================
# CLOUD HOSTING CONFIGURATION
# ============================================================================
# Change this URL to your production deployment URL
PRODUCTION_URL = "https://communal-collage-activity.onrender.com"

# ============================================================================
# LOCAL DEVELOPMENT CONFIGURATION
# ============================================================================
LOCAL_PORT = 5001
LOCAL_URL = f"http://localhost:{LOCAL_PORT}"
LOCAL_URL_ALT = f"http://127.0.0.1:{LOCAL_PORT}"

# ============================================================================
# CORS CONFIGURATION
# ============================================================================
# Allowed origins for CORS - automatically includes production and local URLs
CORS_ORIGINS = [
    LOCAL_URL,
    LOCAL_URL_ALT,
    PRODUCTION_URL,
    # Add any additional frontend domains here if needed
    # "https://your-frontend-domain.com"
]

# ============================================================================
# MINIO CONFIGURATION
# ============================================================================
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'admin')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'password123')
MINIO_SECURE = os.environ.get('MINIO_SECURE', 'false').lower() == 'true'

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================
BUCKET_NAME = "communal-collage"
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
LOCAL_STORAGE_DIR = os.environ.get('LOCAL_STORAGE_DIR', 'local_storage')

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_base_url():
    """Get the base URL for the current environment"""
    return os.environ.get('BASE_URL', PRODUCTION_URL if os.environ.get('FLASK_ENV') == 'production' else LOCAL_URL)

def is_production():
    """Check if running in production"""
    return os.environ.get('FLASK_ENV') == 'production' or os.environ.get('ENVIRONMENT') == 'production'

