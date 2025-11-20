from minio import Minio
import os

class MinIOClient:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key="admin",
            secret_key="password123",
            secure=False
        )
        print("✅ MinIO client initialized")
        
    def ensure_bucket_exists(self, bucket_name):
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f"✅ Bucket '{bucket_name}' created")
            else:
                print(f"✅ Bucket '{bucket_name}' exists")
            return True
        except Exception as e:
            print(f"❌ Bucket error: {e}")
            return False
            
    def upload_image(self, bucket_name, object_name, file_path):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"✅ Uploaded: {object_name}")
            return True
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False
        
    def list_images(self, bucket_name):
        try:
            objects = list(self.client.list_objects(bucket_name))
            print(f"✅ Found {len(objects)} images")
            return objects
        except Exception as e:
            print(f"❌ List failed: {e}")
            return []
        
    def delete_all_images(self, bucket_name):
        try:
            objects = self.list_images(bucket_name)
            for obj in objects:
                self.client.remove_object(bucket_name, obj.object_name)
            print(f"✅ Deleted all images from {bucket_name}")
            return True
        except Exception as e:
            print(f"❌ Delete failed: {e}")
            return False
