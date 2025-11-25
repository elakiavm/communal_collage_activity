from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import os
from datetime import datetime, timedelta
from minio_client import MinIOClient

app = Flask(__name__)
# Configure CORS properly for production
CORS(app, origins=[
    "http://127.0.0.1:5001",          # Local development
    "http://localhost:5001",          # Local development
    "https://communal-collage-activity.onrender.com",  # Your Render URL
    "https://your-frontend-domain.com"  # If you have a separate frontend
])

minio_client = MinIOClient()
BUCKET_NAME = "communal-collage"
minio_client.ensure_bucket_exists(BUCKET_NAME)

daily_tokens = {}

minio_client = MinIOClient()
BUCKET_NAME = "communal-collage"
minio_client.ensure_bucket_exists(BUCKET_NAME)

daily_tokens = {}

@app.route('/')
def serve_upload_page():
    return send_from_directory('.', 'upload.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "server": "Communal Collage API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/generate-token', methods=['POST'])
def generate_token():
    token = str(uuid.uuid4())[:8]
    expiry = datetime.now() + timedelta(hours=24)
    
    daily_tokens[token] = {'expiry': expiry, 'used': False}
    print(f"🎫 Generated token: {token}")
    
    return jsonify({
        "success": True,
        "token": token, 
        "expiry": expiry.isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_image():
    try:
        token = request.form.get('token')
        image = request.files.get('image')
        
        if not token or token not in daily_tokens:
            return jsonify({"success": False, "error": "Invalid token"}), 401
        
        token_data = daily_tokens[token]
        if datetime.now() > token_data['expiry'] or token_data['used']:
            return jsonify({"success": False, "error": "Token expired or used"}), 401
        
        if not image:
            return jsonify({"success": False, "error": "No image"}), 400
        
        # Generate unique filename
        file_ext = image.filename.split('.')[-1].lower() if '.' in image.filename else 'jpg'
        filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = f"temp_uploads/{filename}"
        
        image.save(temp_path)
        
        # Upload to MinIO
        success = minio_client.upload_image(BUCKET_NAME, filename, temp_path)
        
        if success:
            daily_tokens[token]['used'] = True
            os.remove(temp_path)
            return jsonify({
                "success": True,
                "filename": filename,
                "message": "Image uploaded successfully!"
            })
        else:
            return jsonify({"success": False, "error": "Upload failed"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/images', methods=['GET'])
def list_images():
    try:
        objects = minio_client.list_images(BUCKET_NAME)
        images = [{"name": obj.object_name, "size": obj.size} for obj in objects]
        return jsonify({"success": True, "images": images, "count": len(images)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_collage():
    try:
        minio_client.delete_all_images(BUCKET_NAME)
        daily_tokens.clear()
        return jsonify({"success": True, "message": "Collage reset successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Communal Collage Server...")
    print("📱 Access the upload page at: http://localhost:5001")
    print("🗄️  MinIO Admin at: http://localhost:9001")
    app.run(host='0.0.0.0', port=5001, debug=True)
