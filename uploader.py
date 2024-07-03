import os
import boto3
from google.cloud import storage

class FileUploader:
    def __init__(self, s3_bucket_name, gcs_bucket_name, aws_region='us-east-1'):
        self.s3_bucket_name = s3_bucket_name
        self.gcs_bucket_name = gcs_bucket_name

        # AWS S3 setup
        self.s3_client = boto3.client('s3', region_name=aws_region)
        
        # Google Cloud Storage setup
        self.gcs_client = storage.Client()

        # Default file types
        self.s3_file_types = ['jpg', 'png', 'svg', 'webp', 'mp3', 'mp4', 'mpeg4', 'wmv', '3gp', 'webm']
        self.gcs_file_types = ['doc', 'docx', 'csv', 'pdf']
        
    def set_s3_file_types(self, file_types):
        self.s3_file_types = file_types
    
    def set_gcs_file_types(self, file_types):
        self.gcs_file_types = file_types

    def upload_to_s3(self, file_path):
        file_name = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, self.s3_bucket_name, file_name)
        print(f"Uploaded {file_name} to S3 bucket {self.s3_bucket_name}")

    def upload_to_gcs(self, file_path):
        bucket = self.gcs_client.bucket(self.gcs_bucket_name)
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        print(f"Uploaded {file_path} to GCS bucket {self.gcs_bucket_name}")

    def process_directory(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = file.split('.')[-1].lower()
                
                if file_extension in self.s3_file_types:
                    self.upload_to_s3(file_path)
                elif file_extension in self.gcs_file_types:
                    self.upload_to_gcs(file_path)
                else:
                    print(f"File {file} skipped (unsupported type)")

if __name__ == '__main__':
    uploader = FileUploader('your-s3-bucket-name', 'your-gcs-bucket-name')
    uploader.process_directory('your-directory-path')
