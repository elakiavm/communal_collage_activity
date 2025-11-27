from minio import Minio
import os

class MinIOClient:
    def __init__(self):
        # Use environment variables for production, fallback to localhost for development
        self.endpoint = os.environ.get('MINIO_ENDPOINT', 'localhost:9000')
        self.access_key = os.environ.get('MINIO_ACCESS_KEY', 'admin')
        self.secret_key = os.environ.get('MINIO_SECRET_KEY', 'password123')
        self.secure = os.environ.get('MINIO_SECURE', 'false').lower() == 'true'
        
        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )
        self.use_minio = True  # Will be set to False if connection fails
        self.local_storage_dir = os.environ.get('LOCAL_STORAGE_DIR', 'local_storage')
        os.makedirs(self.local_storage_dir, exist_ok=True)
        print(f"✅ MinIO client configured (endpoint: {self.endpoint})")
        
    def ensure_bucket_exists(self, bucket_name):
        if not self.use_minio:
            # For local storage, just ensure the directory exists
            bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
            os.makedirs(bucket_dir, exist_ok=True)
            print(f"✅ Local storage directory '{bucket_name}' ready")
            return True
            
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"✅ Bucket '{bucket_name}' created")
            else:
                print(f"✅ Bucket '{bucket_name}' exists")
            return True
        except Exception as e:
            print(f"❌ Bucket error: {e}")
            print("⚠️  MinIO connection failed, falling back to local file storage")
            self.use_minio = False
            bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
            os.makedirs(bucket_dir, exist_ok=True)
            print(f"✅ Local storage directory '{bucket_name}' ready")
            return True
            
    def upload_image(self, bucket_name, object_name, file_path):
        if not self.use_minio:
            # Fallback to local file storage
            try:
                import shutil
                bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
                os.makedirs(bucket_dir, exist_ok=True)
                dest_path = os.path.join(bucket_dir, object_name)
                shutil.copy2(file_path, dest_path)
                print(f"✅ Uploaded to local storage: {object_name}")
                return True
            except Exception as e:
                print(f"❌ Local upload failed: {e}")
                return False
                
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"✅ Uploaded: {object_name}")
            return True
        except Exception as e:
            print(f"❌ MinIO upload failed: {e}")
            print("⚠️  Falling back to local file storage")
            self.use_minio = False
            # Retry with local storage
            try:
                import shutil
                bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
                os.makedirs(bucket_dir, exist_ok=True)
                dest_path = os.path.join(bucket_dir, object_name)
                shutil.copy2(file_path, dest_path)
                print(f"✅ Uploaded to local storage: {object_name}")
                return True
            except Exception as e2:
                print(f"❌ Local upload also failed: {e2}")
                return False
        
    def list_images(self, bucket_name):
        if not self.use_minio:
            # Fallback to local file storage
            try:
                bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
                if not os.path.exists(bucket_dir):
                    return []
                
                objects = []
                for filename in os.listdir(bucket_dir):
                    file_path = os.path.join(bucket_dir, filename)
                    if os.path.isfile(file_path):
                        # Create a simple object-like structure
                        class LocalObject:
                            def __init__(self, name, size):
                                self.object_name = name
                                self.size = size
                        objects.append(LocalObject(filename, os.path.getsize(file_path)))
                print(f"✅ Found {len(objects)} images in local storage")
                return objects
            except Exception as e:
                print(f"❌ Local list failed: {e}")
                return []
                
        try:
            objects = list(self.client.list_objects(bucket_name))
            print(f"✅ Found {len(objects)} images")
            return objects
        except Exception as e:
            print(f"❌ List failed: {e}")
            return []
        
    def delete_all_images(self, bucket_name):
        if not self.use_minio:
            # Fallback to local file storage
            try:
                import shutil
                bucket_dir = os.path.join(self.local_storage_dir, bucket_name)
                if os.path.exists(bucket_dir):
                    shutil.rmtree(bucket_dir)
                    os.makedirs(bucket_dir, exist_ok=True)
                print(f"✅ Deleted all images from local storage: {bucket_name}")
                return True
            except Exception as e:
                print(f"❌ Local delete failed: {e}")
                return False
                
        try:
            objects = self.list_images(bucket_name)
            for obj in objects:
                self.client.remove_object(bucket_name, obj.object_name)
            print(f"✅ Deleted all images from {bucket_name}")
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
