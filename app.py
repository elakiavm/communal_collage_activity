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

# Ensure temp_uploads directory exists
os.makedirs("temp_uploads", exist_ok=True)

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
    temp_path = None
    try:
        token = request.form.get('token')
        image = request.files.get('image')
        
        if not token or token not in daily_tokens:
            return jsonify({"success": False, "error": "Invalid token"}), 401
        
        token_data = daily_tokens[token]
        if datetime.now() > token_data['expiry'] or token_data['used']:
            return jsonify({"success": False, "error": "Token expired or used"}), 401
        
        if not image:
            return jsonify({"success": False, "error": "No image provided"}), 400
        
        # Check file size (10MB limit)
        image.seek(0, os.SEEK_END)
        file_size = image.tell()
        image.seek(0)  # Reset file pointer
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return jsonify({"success": False, "error": f"File too large. Maximum size is 10MB, got {file_size / 1024 / 1024:.2f}MB"}), 400
        
        # Ensure temp_uploads directory exists
        os.makedirs("temp_uploads", exist_ok=True)
        
        # Generate unique filename
        file_ext = image.filename.split('.')[-1].lower() if '.' in image.filename else 'jpg'
        if file_ext not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            return jsonify({"success": False, "error": f"Invalid file type: {file_ext}. Allowed: jpg, jpeg, png, gif, bmp"}), 400
        
        filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = f"temp_uploads/{filename}"
        
        # Save uploaded file
        try:
            image.save(temp_path)
            print(f"📁 Saved temp file: {temp_path}")
        except Exception as e:
            print(f"❌ Failed to save temp file: {e}")
            return jsonify({"success": False, "error": f"Failed to save file: {str(e)}"}), 500
        
        # Upload to storage (MinIO or local fallback)
        success = minio_client.upload_image(BUCKET_NAME, filename, temp_path)
        
        if success:
            daily_tokens[token]['used'] = True
            # Clean up temp file
            try:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
                    print(f"🗑️  Cleaned up temp file: {temp_path}")
            except Exception as e:
                print(f"⚠️  Failed to remove temp file: {e}")
            
            return jsonify({
                "success": True,
                "filename": filename,
                "message": "Image uploaded successfully!"
            })
        else:
            return jsonify({"success": False, "error": "Upload to storage failed. Please try again."}), 500
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Upload error: {error_trace}")
        
        # Clean up temp file on error
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except:
            pass
        
        return jsonify({
            "success": False, 
            "error": f"Upload failed: {str(e)}"
        }), 500

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
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Communal Collage Server...")
    print(f"📱 Access the upload page at: http://localhost:{port}")
    print("🗄️  MinIO Admin at: http://localhost:9001")
    app.run(host='0.0.0.0', port=port, debug=debug)
