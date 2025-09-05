import boto3
import os

def download_from_s3(bucket, key, dest, aws_conn_id="aws_default"):
    s3 = boto3.client("s3")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    s3.download_file(bucket, key, dest)
    print(f"✅ Downloaded {key} from {bucket} to {dest}")
